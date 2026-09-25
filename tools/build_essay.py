#!/usr/bin/env python3
"""
build_essay.py — Prompted.daily page generator

Takes a structured post spec (posts/<slug>.json) and assembles the on-site
canonical essay page from tools/essay-template.html, then inserts/updates
its homepage card in index.html. Never commits or pushes — that stays a
human-triggered step, per the repo's publishing rules.

Usage:
    python3 tools/build_essay.py posts/<slug>.json
    python3 tools/build_essay.py posts/<slug>.json --dry-run   (build, no write)

Requires Python 3.9+ (the `from __future__ import annotations` line below is
load-bearing — without it, the `dict | None` style type hints in this file
crash on Python < 3.10, which is what a stock macOS python3 usually is).

Spec fields (posts/<slug>.json):
    slug              str, required. Folder name and URL path.
    title             str, required. Also used as <h1> and og:title.
    kicker            str, required. e.g. "AI Safety · Method"
    dek               str, required. Italic subhead under the title.
    date              str, required. e.g. "September 13, 2026"
    meta_description  str, required. <meta name="description">
    og_description    str, optional. Defaults to meta_description.
    read_minutes      int, optional. Auto-estimated from body word count if omitted.
    body_html         str, required. Full essay body as raw HTML (p, h2, blockquote, a, em).
    hero_image        obj, optional. {"src": "<path to source image file>", "alt": "...", "caption": "..."}
                       If omitted, page ships with no hero image (never invented).
    prompt_section    list, required. Ordered blocks, each one of:
                       {"type": "text", "html": "<p>...</p>"}
                       {"type": "prompt", "id": "p1", "label": "the second pass", "text": "raw prompt text"}
    medium_url        str, optional. If present, adds the "Also published on Medium" footer line.
    card_blurb        str, required. One-line homepage card blurb — DRAFT ONLY, needs human approval
                       before this script is run for real (see CLAUDE.md voice rules).
    card_thumb_alt    str, optional. Alt text for the homepage card thumbnail.

This script does not judge whether card_blurb or prompt_section content is any good.
That judgment is the human review step. It only removes the risk of a hand-edit typo
in the surrounding template — canonical tags, card markup, CSS classes.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "tools" / "essay-template.html"
INDEX = REPO / "index.html"

WORDS_PER_MINUTE = 230


def estimate_read_minutes(body_html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", body_html)
    words = len(text.split())
    return max(1, round(words / WORDS_PER_MINUTE))


def render_hero_block(hero: dict | None, slug: str) -> str:
    if not hero:
        return ""
    alt = html.escape(hero.get("alt", ""), quote=True)
    caption = hero.get("caption", "")
    return (
        '<figure style="margin:0;">\n'
        f'      <img class="hero-img" src="header.png" alt="{alt}" />\n'
        f'      <figcaption class="hero-cap">{caption}</figcaption>\n'
        '    </figure>'
    )


def render_prompt_block(block: dict) -> str:
    if block["type"] == "text":
        return f'    <div class="body">\n      {block["html"]}\n    </div>'
    if block["type"] == "prompt":
        text = html.escape(block["text"])
        return (
            '    <div class="promptcard">\n'
            f'      <div class="bar"><span class="label"><span class="caret">▸</span> {block["label"]}</span>'
            f'<button class="copybtn" type="button" data-copy="{block["id"]}">Copy</button></div>\n'
            f'<pre id="{block["id"]}">{text}</pre>\n'
            '    </div>'
        )
    raise ValueError(f"Unknown prompt_section block type: {block['type']}")


def render_prompt_section(blocks: list) -> str:
    return "\n\n".join(render_prompt_block(b) for b in blocks)


def render_syndication(medium_url: str | None) -> str:
    if not medium_url:
        return ""
    return (
        f'<p class="syndicate">Also published on <a href="{medium_url}" '
        f'target="_blank" rel="noopener">Medium</a>. Canonical version lives here.</p>'
    )


def build_page(spec: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    slug = spec["slug"]
    read_minutes = spec.get("read_minutes") or estimate_read_minutes(spec["body_html"])
    og_image = f'https://prompteddaily.com/{slug}/header.png' if spec.get("hero_image") else "https://prompteddaily.com/share.png"

    replacements = {
        "__PAGE_TITLE__": spec["title"],
        "__META_DESCRIPTION__": spec["meta_description"],
        "__SLUG__": slug,
        "__OG_DESCRIPTION__": spec.get("og_description", spec["meta_description"]),
        "__OG_IMAGE__": og_image,
        "__KICKER__": spec["kicker"],
        "__TITLE__": spec["title"],
        "__DEK__": spec["dek"],
        "__READ_MINUTES__": str(read_minutes),
        "__DATE__": spec["date"],
        "__HERO_BLOCK__": render_hero_block(spec.get("hero_image"), slug),
        "__BODY__": spec["body_html"],
        "__PROMPT_SECTION__": render_prompt_section(spec["prompt_section"]),
        "__SYNDICATION_LINE__": render_syndication(spec.get("medium_url")),
    }
    for marker, value in replacements.items():
        if marker not in template:
            raise RuntimeError(f"Template is missing expected marker: {marker}")
        template = template.replace(marker, value)

    leftover = re.findall(r"__[A-Z_]+__", template)
    if leftover:
        raise RuntimeError(f"Unfilled markers remain: {sorted(set(leftover))}")
    return template


def render_card(spec: dict) -> str:
    slug = spec["slug"]
    thumb = ""
    thumb_path = REPO / "img" / f"{slug}.jpg"
    if thumb_path.exists():
        alt = html.escape(spec.get("card_thumb_alt", ""), quote=True)
        thumb = f'\n          <img class="card-thumb" src="/img/{slug}.jpg" alt="{alt}" />'
    return (
        f'        <a class="card reveal" href="/{slug}/">{thumb}\n'
        f'          <span class="kicker">{spec["kicker"]}</span>\n'
        f'          <h3>{spec["title"]}</h3>\n'
        f'          <p>{spec["card_blurb"]}</p>\n'
        f'          <span class="read">Read + run the prompt</span>\n'
        f'        </a>'
    )


def _split_cards_grid(index_html: str) -> tuple[str, str, str]:
    """Return (before, grid_inner, after) split around the .cards grid only.
    The grid contains no nested <div> (verified against the real markup), so
    the first </div> after the opening tag reliably closes it — this is what
    keeps this function from ever touching the hero-featured block, which
    lives in a different part of the page and can share the same href."""
    marker = '<div class="cards">'
    start = index_html.find(marker)
    if start == -1:
        raise RuntimeError("Could not find the .cards grid opening tag in index.html")
    inner_start = start + len(marker)
    close = index_html.find("</div>", inner_start)
    if close == -1:
        raise RuntimeError("Could not find the .cards grid's closing tag")
    return index_html[:inner_start], index_html[inner_start:close], index_html[close:]


def upsert_card(spec: dict, dry_run: bool) -> str:
    index_html = INDEX.read_text(encoding="utf-8")
    slug = spec["slug"]
    before, grid, after = _split_cards_grid(index_html)

    # Remove any existing archive card for this slug so re-runs are idempotent.
    # Scoped to `grid` only — the hero-featured block for the same slug lives
    # outside this substring entirely and is never touched here.
    card_pattern = re.compile(
        r'\n?        <a class="card reveal" href="/' + re.escape(slug) + r'/">.*?</a>\n?',
        re.DOTALL,
    )
    href_marker = f'href="/{slug}/"'
    if href_marker in grid and not card_pattern.search(grid):
        raise RuntimeError(
            f"Found an archive-grid href for {slug} but couldn't isolate its card "
            "block — stopping rather than risk corrupting the grid. Fix by hand."
        )
    grid = card_pattern.sub("\n", grid)

    new_card = render_card(spec)
    grid = "\n\n" + new_card + grid

    index_html = before + grid + after
    if not dry_run:
        INDEX.write_text(index_html, encoding="utf-8")
    return new_card


def render_latest(spec: dict) -> str:
    slug = spec["slug"]
    thumb_path = REPO / "img" / f"{slug}.jpg"
    img_tag = ""
    if thumb_path.exists():
        alt = html.escape(spec.get("card_thumb_alt", ""), quote=True)
        img_tag = f'<img class="card-thumb" src="/img/{slug}.jpg" alt="{alt}" />\n        '
    return (
        f'<a href="/{slug}/" class="card hero-featured reveal">\n'
        f'        <span class="hero-featured-tag">Latest</span>\n'
        f'        {img_tag}<span class="kicker">{spec["kicker"]}</span>\n'
        f'        <h3>{spec["title"]}</h3>\n'
        f'        <p>{spec["card_blurb"]}</p>\n'
        f'        <span class="read">Read + run the prompt</span>\n'
        '      </a>'
    )


def upsert_latest(spec: dict, dry_run: bool) -> str | None:
    """Point the homepage hero at this post, since it's the one just published.
    Silently does nothing if the hero markers don't exist yet — the hero is a
    deliberate one-time addition (see the homepage redesign), not something
    every repo is assumed to have."""
    index_html = INDEX.read_text(encoding="utf-8")
    start_marker, end_marker = "<!-- LATEST:START -->", "<!-- LATEST:END -->"
    start = index_html.find(start_marker)
    end = index_html.find(end_marker)
    if start == -1 or end == -1:
        return None
    end += len(end_marker)
    new_block = f"{start_marker}\n      {render_latest(spec)}\n      {end_marker}"
    index_html = index_html[:start] + new_block + index_html[end:]
    if not dry_run:
        INDEX.write_text(index_html, encoding="utf-8")
    return new_block


def process_hero_image(spec: dict, dry_run: bool) -> None:
    hero = spec.get("hero_image")
    if not hero or not hero.get("src"):
        return
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is required for hero image processing: pip install Pillow --break-system-packages")

    slug = spec["slug"]
    src_path = Path(hero["src"]).expanduser()
    if not src_path.exists():
        sys.exit(f"hero_image.src not found: {src_path}")

    out_dir = REPO / slug
    header_dst = out_dir / "header.png"
    thumb_dst = REPO / "img" / f"{slug}.jpg"

    im = Image.open(src_path).convert("RGB")
    if dry_run:
        print(f"--- Would write: {header_dst}, {thumb_dst} (from {src_path}) ---")
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    (REPO / "img").mkdir(parents=True, exist_ok=True)
    im.save(header_dst, "PNG", optimize=True)

    w, h = im.size
    t = 16 / 9
    if w / h > t:
        nw = int(h * t)
        x = (w - nw) // 2
        crop = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / t)
        y = (h - nh) // 2
        crop = im.crop((0, y, w, y + nh))
    crop.resize((640, 360), Image.LANCZOS).save(thumb_dst, "JPEG", quality=82, optimize=True)
    print(f"Wrote {header_dst} and {thumb_dst}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec_path", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Build and report, but write nothing.")
    args = parser.parse_args()

    spec = json.loads(args.spec_path.read_text(encoding="utf-8"))
    required = ["slug", "title", "kicker", "dek", "date", "meta_description", "body_html", "prompt_section", "card_blurb"]
    missing = [f for f in required if f not in spec]
    if missing:
        sys.exit(f"Spec is missing required fields: {missing}")

    process_hero_image(spec, args.dry_run)

    page_html = build_page(spec)
    out_dir = REPO / spec["slug"]

    print(f"--- Would write: {out_dir / 'index.html'} ({len(page_html)} bytes) ---")
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page_html, encoding="utf-8")
        print(f"Wrote {out_dir / 'index.html'}")

    card_html = upsert_card(spec, args.dry_run)
    print("--- Homepage card (archive grid) ---")
    print(card_html)

    latest_html = upsert_latest(spec, args.dry_run)
    if latest_html is not None:
        print("--- Homepage hero (now points here) ---")
        print(latest_html)
    else:
        print("--- Homepage hero: no LATEST markers found, left untouched ---")

    if args.dry_run:
        print("\n(dry run — index.html not modified)")
    else:
        print(f"Updated {INDEX}")

    print(
        "\nNothing has been committed or pushed. Review the rendered page and the "
        "card above — especially card_blurb and any prompt_section block — before "
        "running git add / commit / push."
    )


if __name__ == "__main__":
    main()
