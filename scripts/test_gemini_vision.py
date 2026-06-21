"""Test Gemini vision via REST and SDK."""
import base64
import json
import time
import urllib.error
import urllib.request
from io import BytesIO

from PIL import Image

from app.config import GEMINI_CONFIG

TIMEOUT = 30


def make_jpeg() -> bytes:
    img = Image.new("RGB", (400, 300), color=(34, 120, 40))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_rest_vision(image_bytes: bytes) -> None:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_CONFIG.model}:generateContent"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Describe this plant image in one sentence."},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": base64.b64encode(image_bytes).decode("ascii"),
                        }
                    },
                ]
            }
        ],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_CONFIG.api_key,
        },
        method="POST",
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            print(f"REST vision OK in {time.perf_counter() - start:.1f}s")
            print(body[:400])
    except Exception as exc:
        print(f"REST vision FAIL in {time.perf_counter() - start:.1f}s: {exc}")


def test_sdk_vision(image_bytes: bytes) -> None:
    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=GEMINI_CONFIG.api_key,
        http_options=types.HttpOptions(timeout=TIMEOUT * 1000),
    )
    start = time.perf_counter()
    try:
        response = client.models.generate_content(
            model=GEMINI_CONFIG.model,
            contents=[
                "Describe this plant image in one sentence as JSON with visual_summary field.",
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        print(f"SDK vision OK in {time.perf_counter() - start:.1f}s")
        print((response.text or "")[:400])
    except Exception as exc:
        print(f"SDK vision FAIL in {time.perf_counter() - start:.1f}s: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    image = make_jpeg()
    print("image bytes:", len(image))
    print("--- REST vision ---")
    test_rest_vision(image)
    print("--- SDK vision ---")
    test_sdk_vision(image)
