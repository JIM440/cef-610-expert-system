"""
Gemini vision analyzer - maps uploaded crop images to symptoms in the database.
"""

import json
import re
from difflib import get_close_matches
from io import BytesIO

from google import genai
from google.genai import types
from google.genai.errors import APIError
from PIL import Image

from app.config import GEMINI_CONFIG
from app.repositories.symptom_repository import get_all_symptoms

MIME_BY_EXT = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}

GEMINI_TIMEOUT_SECONDS = 30
GEMINI_MAX_IMAGE_PX = 1024
FALLBACK_MODELS = ("gemini-2.0-flash", "gemini-2.5-flash")


def _build_prompt(symptoms: list[dict]) -> str:
    catalog = "\n".join(
        f'- id={s["id"]}, name="{s["name"]}": {s["description"]}'
        for s in symptoms
    )
    return f"""You are an agricultural expert analyzing tomato crop disease images.

Our symptom database (ONLY choose from this list):
{catalog}

Examine the image and identify visible symptoms from the catalog above.

Return valid JSON only, with this exact shape:
{{
  "visual_summary": "Brief description of what you see in the image",
  "detected_symptoms": [
    {{"symptom_id": <id from catalog>, "symptom_name": "<exact name>", "confidence": <0-100>}}
  ]
}}

Rules:
- symptom_id and symptom_name must match one catalog entry exactly
- Only include symptoms you can reasonably see; omit uncertain ones
- confidence is your certainty (0-100) that the symptom is present
- If nothing matches, return an empty detected_symptoms array
"""


def _parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def _mime_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "jpeg"
    return MIME_BY_EXT.get(ext, "image/jpeg")


def _prepare_image(image_bytes: bytes, original_filename: str) -> tuple[bytes, str, Image.Image]:
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image.thumbnail((GEMINI_MAX_IMAGE_PX, GEMINI_MAX_IMAGE_PX))
    mime = _mime_type(original_filename)
    fmt = "PNG" if mime == "image/png" else "JPEG"
    buf = BytesIO()
    image.save(buf, format=fmt, quality=85)
    return buf.getvalue(), mime, image


def _models_to_try() -> list[str]:
    """Prefer stable flash models; gemini-flash-latest often returns 503/timeouts."""
    models: list[str] = []
    for name in ("gemini-2.0-flash", "gemini-2.5-flash", GEMINI_CONFIG.model):
        if name and name not in models:
            models.append(name)
    return models


def _gemini_client() -> genai.Client:
    return genai.Client(
        api_key=GEMINI_CONFIG.api_key,
        http_options=types.HttpOptions(
            timeout=GEMINI_TIMEOUT_SECONDS * 1000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )


def _friendly_api_error(exc: APIError) -> str:
    message = str(exc)
    if "503" in message or "high demand" in message.lower() or "UNAVAILABLE" in message:
        return (
            "Gemini is temporarily busy (high demand). "
            "Please wait a few seconds and try again."
        )
    if "429" in message or "quota" in message.lower():
        return "Gemini rate limit reached. Please wait a moment and try again."
    if "timeout" in message.lower():
        return "Gemini took too long to respond. Please try again with a smaller/clearer image."
    if "401" in message or "403" in message or "API key" in message:
        return "Gemini API key was rejected. Check GEMINI_API_KEY in your .env file."
    return f"Gemini API error: {message}"


def _call_gemini(
    client: genai.Client,
    model: str,
    prompt: str,
    image_bytes: bytes,
    mime_type: str,
):
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    return client.models.generate_content(
        model=model,
        contents=[prompt, image_part],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )


def _clean_name(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _resolve_symptom_id(item: dict, valid_ids: set[int], id_by_name: dict[str, int]) -> int | None:
    sid = item.get("symptom_id")
    if isinstance(sid, int) and sid in valid_ids:
        return sid

    name = _clean_name(item.get("symptom_name"))
    if not name:
        return None
    if name in id_by_name:
        return id_by_name[name]
    matches = get_close_matches(name, list(id_by_name.keys()), n=1, cutoff=0.72)
    return id_by_name[matches[0]] if matches else None


def analyze_image_with_gemini(image_bytes: bytes, original_filename: str = "upload.jpg") -> dict:
    if not GEMINI_CONFIG.is_configured:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file to use image recognition."
        )

    symptoms = get_all_symptoms()
    if not symptoms:
        raise RuntimeError("No symptoms found in the database.")

    valid_ids = {s["id"] for s in symptoms}
    name_by_id = {s["id"]: s["name"] for s in symptoms}
    id_by_name = {_clean_name(s["name"]): s["id"] for s in symptoms}
    prepared_bytes, mime_type, preview = _prepare_image(image_bytes, original_filename)
    prompt = _build_prompt(symptoms)
    client = _gemini_client()

    response = None
    last_error: Exception | None = None
    for model in _models_to_try():
        try:
            response = _call_gemini(client, model, prompt, prepared_bytes, mime_type)
            break
        except APIError as exc:
            last_error = exc
            continue
        except Exception as exc:
            last_error = exc
            if "timeout" in str(exc).lower():
                continue
            break

    if response is None:
        if isinstance(last_error, APIError):
            raise RuntimeError(_friendly_api_error(last_error)) from last_error
        if last_error:
            raise RuntimeError(f"Gemini request failed: {last_error}") from last_error
        raise RuntimeError("Gemini request failed with no response.")

    raw = response.text or ""
    if not raw.strip():
        raise RuntimeError("Gemini returned an empty response.")

    payload = _parse_json_response(raw)
    visual_summary = str(payload.get("visual_summary", "")).strip()
    detected_raw = payload.get("detected_symptoms") or []

    detected: list[dict] = []
    seen_ids: set[int] = set()
    for item in detected_raw:
        if not isinstance(item, dict):
            continue
        sid = _resolve_symptom_id(item, valid_ids, id_by_name)
        if sid is None or sid in seen_ids:
            continue
        confidence = item.get("confidence", 0)
        try:
            score = float(confidence)
        except (TypeError, ValueError):
            score = 0.0
        detected.append(
            {
                "symptom_id": sid,
                "symptom_name": name_by_id[sid],
                "score": round(max(0.0, min(score, 100.0)), 1),
            }
        )
        seen_ids.add(sid)

    detected.sort(key=lambda x: x["score"], reverse=True)

    summary = (
        f"Gemini analysis: {visual_summary}"
        if visual_summary
        else (
            "Detected from image: " + ", ".join(d["symptom_name"] for d in detected)
            if detected
            else "No matching symptoms identified in the image."
        )
    )

    return {
        "symptom_ids": [d["symptom_id"] for d in detected],
        "detected_symptoms": detected,
        "visual_summary": visual_summary,
        "analysis_summary": summary,
        "preview_image": preview,
        "analysis_source": "gemini",
    }
