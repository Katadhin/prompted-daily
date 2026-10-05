#!/usr/bin/env python3
"""
make_images.py — Prompted.daily image pass

Takes the base render from Gemini and produces the two image outputs a piece needs:

    /<slug>/header.png     16:9, wordmark bottom-left (the overlay pass from VISUAL-SYSTEM.md)
    /img/<slug>.jpg        640x360 homepage card thumbnail, ~q82, under 100 KB

Gemini supplies texture only (it garbles text), so this script never invents or edits the
scene. It crops, resizes, adds the Prompted.daily wordmark, and writes the thumbnail. It
refuses to overwrite existing files unless --force is given, and it never touches git.

Usage:
    python3 tools/make_images.py <slug> <source-image>
    python3 tools/make_images.py <slug> <source-image> --dry-run
    python3 tools/make_images.py <slug> <source-image> --no-wordmark
    python3 tools/make_images.py <slug> <source-image> --force

Requires Pillow (pip install Pillow --break-system-packages).
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
WORDMARK = REPO / "img" / "wordmark.png"

MAX_WIDTH = 2752          # matches existing Gemini exports
MIN_WIDTH = 1600          # below this a 16:9 header looks soft on retina
THUMB_SIZE = (640, 360)
THUMB_BUDGET = 100 * 1024  # CLAUDE.md: target well under 100 KB
WORDMARK_WIDTH_FRAC = 0.17  # wordmark width as a share of header width
MARGIN_FRAC = 0.032         # left/bottom margin as a share of header width
BG = (16, 16, 36)           # --bg #101024


def crop_16_9(im: Image.Image) -> Image.Image:
    w, h = im.size
    target = 16 / 9
    if w / h > target:
        nw = int(h * target)
        x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / target)
    y = (h - nh) // 2
    return im.crop((0, y, w, y + nh))


def add_wordmark(im: Image.Image) -> Image.Image:
    """Soft dark vignette in the lower-left for legibility, then the wordmark on top."""
    if not WORDMARK.exists():
        sys.exit(f"Missing {WORDMARK}. Cannot add the wordmark.")
    base = im.convert("RGBA")
    w, h = base.size

    # Vignette: alpha falls off with distance from the bottom-left corner.
    grad = Image.new("L", (w, h), 0)
    px = grad.load()
    rx, ry = w * 0.46, h * 0.30
    x0 = int(w * 0.5)
    y0 = int(h * 0.6)
    for y in range(y0, h):
        dy = (y - h) / ry
        for x in range(0, x0):
            dx = x / rx
            d = (dx * dx + dy * dy) ** 0.5
            if d < 1:
                px[x, y] = int(150 * (1 - d) ** 1.6)
    shade = Image.new("RGBA", (w, h), BG + (0,))
    shade.putalpha(grad)
    base = Image.alpha_composite(base, shade)

    wm = Image.open(WORDMARK).convert("RGBA")
    target_w = int(w * WORDMARK_WIDTH_FRAC)
    target_h = int(wm.height * target_w / wm.width)
    wm = wm.resize((target_w, target_h), Image.LANCZOS)
    margin = int(w * MARGIN_FRAC)
    base.alpha_composite(wm, (margin, h - margin - target_h))
    return base.convert("RGB")


def encode_thumb(im: Image.Image) -> bytes:
    thumb = im.resize(THUMB_SIZE, Image.LANCZOS)
    for q in (82, 78, 74, 70, 66):
        buf = io.BytesIO()
        thumb.save(buf, "JPEG", quality=q, optimize=True)
        if buf.tell() <= THUMB_BUDGET:
            return buf.getvalue()
    sys.exit("Thumbnail will not fit under 100 KB even at q66. Check the source image.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug")
    ap.add_argument("source")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-wordmark", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    src = Path(args.source).expanduser()
    if not src.exists():
        sys.exit(f"Source image not found: {src}")
    page_dir = REPO / args.slug
    header_out = page_dir / "header.png"
    thumb_out = REPO / "img" / f"{args.slug}.jpg"

    for out in (header_out, thumb_out):
        if out.exists() and not args.force:
            sys.exit(f"{out.relative_to(REPO)} already exists. Use --force to overwrite.")

    im = Image.open(src).convert("RGB")
    if im.width < MIN_WIDTH:
        print(f"Warning: source is {im.width}px wide; expect a soft header.", file=sys.stderr)

    im = crop_16_9(im)
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(MAX_WIDTH * 9 / 16)), Image.LANCZOS)
    header = im if args.no_wordmark else add_wordmark(im)
    thumb_bytes = encode_thumb(header)

    print(f"header : {header_out.relative_to(REPO)}  {header.width}x{header.height}"
          f"  wordmark={'no' if args.no_wordmark else 'yes'}")
    print(f"thumb  : {thumb_out.relative_to(REPO)}  {THUMB_SIZE[0]}x{THUMB_SIZE[1]}  {len(thumb_bytes) / 1024:.1f} KB")
    if args.dry_run:
        print("Dry run: nothing written.")
        return

    page_dir.mkdir(parents=True, exist_ok=True)
    header.save(header_out, "PNG", optimize=True)
    thumb_out.write_bytes(thumb_bytes)
    print("Written. Next: set hero_image in the post spec and rerun tools/build_essay.py.")


if __name__ == "__main__":
    main()
