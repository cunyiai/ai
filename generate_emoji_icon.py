#!/usr/bin/env python3
"""
Generate app launcher icons from 🩺 (stethoscope) emoji for all densities.
Replaces ic_launcher.webp, ic_launcher_round.webp, ic_launcher_foreground.webp
in app/src/main/res/mipmap-*/ directories.
"""

import os
import sys
import urllib.request
import tempfile

from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(PROJECT_ROOT, "app", "src", "main", "res")

# Emoji codepoint for 🩺 (stethoscope) = U+1FA7A
# Try multiple sources
EMOJI_URLS = [
    "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u1fa7a.png",
    "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72/1fa7a.png",
    "https://em-content.zobj.net/source/apple/391/stethoscope_1f3a.png",
]

# Android launcher icon sizes by density (px)
# Regular & round icons
ICON_SIZES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

# Adaptive icon foreground layer is 108x108 dp (full size),
# but the visible icon area is 72x72 dp centered.
# We'll generate a 108x108 foreground with the emoji fitted to ~72x72 area.
FOREGROUND_SIZE = 108
FOREGROUND_ICON_AREA = 72


def download_emoji_image():
    """Try to download emoji PNG from multiple sources."""
    for url in EMOJI_URLS:
        try:
            print(f"  Trying: {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = resp.read()
                    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                        tmp.write(data)
                        tmp_path = tmp.name
                    print(f"  ✓ Downloaded to {tmp_path}")
                    return tmp_path
        except Exception as e:
            print(f"  ✗ Failed: {e}")
    return None


def generate_stethoscope_icon(size):
    """Generate a simple stethoscope-like icon as fallback."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    # Draw a simple circle with a stethoscope-like shape
    # Use a blue color (#4A90D9)
    color = (74, 144, 217)
    margin = int(size * 0.15)
    # Draw circle (the chest piece)
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        outline=color,
        width=max(int(size * 0.06), 2),
    )
    # Draw a line (the tube)
    center = size // 2
    draw.line(
        [(center, margin + int(size * 0.15)), (center, size - margin)],
        fill=color,
        width=max(int(size * 0.06), 2),
    )
    return img


def main():
    print("=== Generating 🩺 app icons ===")

    # Step 1: Try to download emoji image
    print("\n[1] Downloading emoji image...")
    emoji_path = download_emoji_image()

    if emoji_path:
        try:
            base_img = Image.open(emoji_path).convert("RGBA")
            print(f"  ✓ Loaded emoji image: {base_img.size}")
        except Exception as e:
            print(f"  ✗ Failed to load image: {e}")
            emoji_path = None

    if not emoji_path:
        print("  No emoji image downloaded, using generated stethoscope icon...")
        # Generate a 512x512 base image
        base_img = generate_stethoscope_icon(512)
        print("  ✓ Generated base icon (512x512)")

    # Step 2: Generate icons for each density
    print("\n[2] Generating icons for each density...")
    for density, size in ICON_SIZES.items():
        mipmap_dir = os.path.join(RES_DIR, f"mipmap-{density}")
        if not os.path.isdir(mipmap_dir):
            print(f"  ⚠ {mipmap_dir} not found, skipping...")
            continue

        # Resize for regular & round icons
        img_resized = base_img.resize((size, size), Image.LANCZOS)

        # Save as .webp (replacing existing .webp files)
        for icon_name in ["ic_launcher.webp", "ic_launcher_round.webp"]:
            icon_path = os.path.join(mipmap_dir, icon_name)
            if os.path.exists(icon_path) or True:  # Overwrite or create
                img_resized.save(icon_path, "WEBP", quality=90)
                print(f"  ✓ {icon_path}")

        # Foreground layer: 108x108 for adaptive icons
        fg_size = FOREGROUND_SIZE
        fg_img = base_img.resize((FOREGROUND_ICON_AREA, FOREGROUND_ICON_AREA), Image.LANCZOS)
        fg_canvas = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
        offset = (fg_size - FOREGROUND_ICON_AREA) // 2
        fg_canvas.paste(fg_img, (offset, offset), fg_img if fg_img.mode == "RGBA" else None)

        fg_path = os.path.join(mipmap_dir, "ic_launcher_foreground.webp")
        fg_canvas.save(fg_path, "WEBP", quality=90)
        print(f"  ✓ {fg_path}")

    print("\n[3] Done! Icons generated for all densities.")
    print("  Next: run ./gradlew assembleDebug to build APK with new icon.")


if __name__ == "__main__":
    main()
