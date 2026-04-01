"""
Usage:
  python main.py --prompt "a futuristic city at sunset"
  python main.py --image path/to/photo.png
  python main.py --prompt "oil painting of a dog" --size 1792x1024
"""

import argparse
from generator import generate_from_prompt, generate_from_image


def main():
    parser = argparse.ArgumentParser(description="AI Photo Generator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", type=str, help="Text prompt to generate image from")
    group.add_argument("--image",  type=str, help="Path to existing image for variation")
    parser.add_argument("--size",  type=str, default="1024x1024",
                        help="Image size: 1024x1024 | 1792x1024 | 1024x1792 (prompt only)")
    args = parser.parse_args()

    if args.prompt:
        output = generate_from_prompt(args.prompt, size=args.size)
    else:
        output = generate_from_image(args.image)

    print(f"\nDone. Image saved to: {output}")


if __name__ == "__main__":
    main()
