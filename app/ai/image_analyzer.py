"""
Image symptom analysis entry point — uses Gemini vision when configured.
"""

from app.ai.gemini_analyzer import analyze_image_with_gemini


def analyze_image_bytes(image_bytes: bytes, original_filename: str = "upload.jpg") -> dict:
    return analyze_image_with_gemini(image_bytes, original_filename)
