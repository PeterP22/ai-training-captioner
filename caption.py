#!/usr/bin/env python3
"""
LoRA Training Image Captioner
Auto-caption images using GPT-5 Mini for high-quality LoRA training

Usage:
  python caption.py --folder /path/to/images --trigger YOUR_TRIGGER_WORD
"""

import os
import base64
import argparse
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package required")
    print("Run: pip install openai")
    exit(1)

# Caption prompt optimized for LoRA training
CAPTION_PROMPT = """Describe this photo for AI image model training. Focus on:

1. APPEARANCE: clothing, hair style, facial expression, pose, body position
2. SETTING: location, background, environment
3. LIGHTING: natural/artificial, direction, mood
4. PHOTO STYLE: candid, portrait, action shot, etc.

DO NOT describe:
- Specific facial features (the model learns these from the image)
- Race, ethnicity, or age estimates
- Subjective attractiveness judgments

Write as a single flowing description. Start with: "a photo of {trigger},"

Example:
"a photo of {trigger}, wearing a fitted navy henley shirt, standing outdoors with arms crossed, confident relaxed expression, golden hour sunlight from the left, urban park background with blurred trees, candid lifestyle photography style"
"""


def encode_image(image_path: str) -> str:
    """Convert image to base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def get_mime_type(image_path: str) -> str:
    """Get MIME type from extension"""
    ext = Path(image_path).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")


def caption_image(client: OpenAI, image_path: str, trigger: str, model: str) -> str:
    """Generate caption for a single image using OpenAI Responses API"""
    base64_image = encode_image(image_path)
    mime_type = get_mime_type(image_path)
    prompt = CAPTION_PROMPT.replace("{trigger}", trigger)

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": f"data:{mime_type};base64,{base64_image}"},
                ],
            }
        ],
    )

    caption = response.output_text.strip()

    # Ensure caption starts with trigger
    if not caption.lower().startswith(f"a photo of {trigger.lower()}"):
        caption = f"a photo of {trigger}, {caption}"

    return caption


def process_folder(folder: str, trigger: str, model: str, preview: bool = False, overwrite: bool = False):
    """Process all images in folder"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Export it: export OPENAI_API_KEY=sk-...")
        exit(1)

    client = OpenAI(api_key=api_key)
    folder_path = Path(folder)

    if not folder_path.exists():
        print(f"Error: Folder not found: {folder}")
        exit(1)

    # Find images
    extensions = ('.jpg', '.jpeg', '.png', '.webp')
    images = sorted([f for f in folder_path.iterdir() if f.suffix.lower() in extensions])

    if not images:
        print(f"No images found in {folder}")
        exit(1)

    print(f"{'=' * 50}")
    print(f"LoRA Image Captioner")
    print(f"{'=' * 50}")
    print(f"Folder: {folder}")
    print(f"Images: {len(images)}")
    print(f"Trigger: {trigger}")
    print(f"Model: {model}")
    print(f"Mode: {'Preview' if preview else 'Save'}")
    print(f"{'=' * 50}\n")

    success, skipped, failed = 0, 0, 0

    for i, img_path in enumerate(images, 1):
        caption_path = img_path.with_suffix('.txt')

        if caption_path.exists() and not overwrite and not preview:
            print(f"[{i}/{len(images)}] {img_path.name} - SKIPPED (exists)")
            skipped += 1
            continue

        print(f"[{i}/{len(images)}] {img_path.name}...", end=" ", flush=True)

        try:
            caption = caption_image(client, str(img_path), trigger, model)
            print("OK")
            print(f"    {caption[:80]}{'...' if len(caption) > 80 else ''}")

            if not preview:
                caption_path.write_text(caption)

            success += 1
        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Done! Captioned: {success}, Skipped: {skipped}, Failed: {failed}")
    if not preview:
        print(f"Caption files saved to: {folder}/")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-caption images for LoRA training using GPT-5 Mini",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python caption.py --folder ./my_photos --trigger MYTRIGGER
  python caption.py --folder ./my_photos --trigger MYTRIGGER --preview
  python caption.py --folder ./my_photos --trigger MYTRIGGER --overwrite
        """
    )
    parser.add_argument("--folder", "-f", required=True, help="Path to folder containing images")
    parser.add_argument("--trigger", "-t", required=True, help="Trigger word for your LoRA (e.g., MYTRIGGER)")
    parser.add_argument("--model", "-m", default="gpt-5-mini", help="OpenAI model (default: gpt-5-mini)")
    parser.add_argument("--preview", "-p", action="store_true", help="Preview captions without saving")
    parser.add_argument("--overwrite", "-o", action="store_true", help="Overwrite existing caption files")

    args = parser.parse_args()
    process_folder(args.folder, args.trigger, args.model, args.preview, args.overwrite)


if __name__ == "__main__":
    main()
