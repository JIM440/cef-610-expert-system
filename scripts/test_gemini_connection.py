"""Quick Gemini connectivity diagnostic."""
import json
import time
import urllib.error
import urllib.request

from app.config import GEMINI_CONFIG

TIMEOUT = 20


def test_rest_text() -> None:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_CONFIG.model}:generateContent"
    )
    payload = {
        "contents": [{"parts": [{"text": "Reply with exactly: OK"}]}],
        "generationConfig": {"responseMimeType": "text/plain"},
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
            elapsed = time.perf_counter() - start
            print(f"REST OK in {elapsed:.1f}s")
            print(body[:300])
    except urllib.error.HTTPError as exc:
        elapsed = time.perf_counter() - start
        err = exc.read().decode("utf-8", errors="replace")
        print(f"REST HTTP {exc.code} in {elapsed:.1f}s")
        print(err[:500])
    except Exception as exc:
        elapsed = time.perf_counter() - start
        print(f"REST failed in {elapsed:.1f}s: {type(exc).__name__}: {exc}")


def test_sdk_text() -> None:
    from google import genai

    client = genai.Client(api_key=GEMINI_CONFIG.api_key)
    start = time.perf_counter()
    try:
        response = client.models.generate_content(
            model=GEMINI_CONFIG.model,
            contents="Reply with exactly: OK",
        )
        elapsed = time.perf_counter() - start
        print(f"SDK OK in {elapsed:.1f}s -> {(response.text or '').strip()[:80]}")
    except Exception as exc:
        elapsed = time.perf_counter() - start
        print(f"SDK failed in {elapsed:.1f}s: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    print("model:", GEMINI_CONFIG.model)
    print("key prefix:", GEMINI_CONFIG.api_key[:6] + "...")
    print("--- REST ---")
    test_rest_text()
    print("--- SDK ---")
    test_sdk_text()
