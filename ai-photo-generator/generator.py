"""
AI Photo Generator
- Text prompt → image  (DALL-E 3)
- Existing image → variation or edit  (DALL-E 2 image variation)
"""

import os
import base64
import requests
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_from_prompt(prompt: str, size: str = "1024x1024") -> Path:
    """
    Text prompt → image using DALL-E 3.
    Sizes: 1024x1024, 1792x1024, 1024x1792
    """
    print(f"Generating from prompt: {prompt!r}")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    url = response.data[0].url
    return _download(url, prefix="prompt")


def generate_from_image(image_path: str) -> Path:
    """
    Existing image → variation using DALL-E 2.
    Image must be square PNG, max 4MB.
    """
    image_path = Path(image_path)
    print(f"Generating variation from: {image_path.name}")
    with open(image_path, "rb") as f:
        response = client.images.create_variation(
            image=f,
            n=1,
            size="1024x1024",
        )
    url = response.data[0].url
    return _download(url, prefix="variation")


def _download(url: str, prefix: str) -> Path:
    """Download image from URL and save to output/."""
    import time
    filename = OUTPUT_DIR / f"{prefix}_{int(time.time())}.png"
    data = requests.get(url).content
    filename.write_bytes(data)
    print(f"Saved → {filename}")
    return filename
