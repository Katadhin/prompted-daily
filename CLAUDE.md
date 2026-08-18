# CLAUDE.md — Prompted.daily

Instructions for working in this repo. Read before editing anything.

## What this is
A static website published via GitHub Pages. No build step, no framework, no
dependencies — every page is hand-written HTML with embedded CSS. Live at
https://prompteddaily.com.

Prompted pairs an analytical essay with the engineered prompt that produced it.
The prompt is the product, not decoration. Tagline: "Don't just read the news.
Engage with it."

## Domain facts — do NOT "fix" these
- Live domain is **prompteddaily.com**. Use it in every canonical tag, OG url, and
  absolute internal link.
- The wordmark renders as "Prompted.daily" with an amber period. That is deliberate
  stylization, not the URL. Do not change it to match the domain.
- `.daily` is not a real TLD; `prompted.daily` is a dead link. Never use it anywhere.
- `CNAME` must contain exactly `prompteddaily.com`. Never overwrite it.

## Repo structure
```
/index.html                          homepage: hero, idea, prompt, archive, about
/<slug>/index.html                   one folder per essay — the on-site canonical version
/<slug>/header.png                   that essay's header image
/img/<slug>.jpg                      homepage card thumbnails (light, optimized)
/CNAME                               prompteddaily.com
/.nojekyll                           serve files as-is
/CLAUDE.md /README.md                this file + deploy notes
/VISUAL-SYSTEM.md /COWORK-AUTOMATION.md   internal playbooks
```

## Git / publishing
- Deploy is automatic: push to `main`, GitHub Pages rebuilds in ~1 min. No CI.
- Flow: edit → `git add -A` → `git commit -m "..."` → `git push`.
- Confirm with the user before pushing — publishing is public.
- After changing a live essay's canonical URL, the matching Medium post's canonical
  link must be updated by hand in Medium's UI. Remind the user; it can't be scripted.

## Voice standards — any copy you write (card blurbs, deks, microcopy)
- No sentence opens with "I".
- Minimal em-dashes.
- Active prose. Specific over general. Mechanism over headline.
- No bullet lists inside essay bodies.
- Smart-colleague energy.
- Card blurbs and kickers are the USER'S editorial voice. Draft them, then flag for
  approval — never finalize silently.

## Task: add a homepage card thumbnail
1. Get the source image (user provides, or generate per VISUAL-SYSTEM.md).
2. Crop to 16:9, resize to 640x360, save optimized JPEG (~q82) at `/img/<slug>.jpg`.
   Target well under 100 KB.
3. In `index.html`, add as the FIRST child of the matching `.card`:
   `<img class="card-thumb" src="/img/<slug>.jpg" alt="...">`
4. Cards without a thumbnail must still render cleanly — never leave a broken `<img>`.

Crop snippet:
```python
from PIL import Image
im = Image.open(SRC).convert('RGB'); w,h = im.size; t = 16/9
if w/h > t: nw=int(h*t); x=(w-nw)//2; im=im.crop((x,0,x+nw,h))
else: nh=int(w/t); y=(h-nh)//2; im=im.crop((0,y,w,y+nh))
im.resize((640,360), Image.LANCZOS).save(DST,'JPEG',quality=82,optimize=True)
```

## Task: migrate a Medium essay onto the site
1. Get the essay text + its engineered prompt(s) from the user (or a Medium URL).
2. Copy an existing `<slug>/index.html` (e.g. `the-conversation-was-compounding`) as
   the template. Keep all styling and the copy-button JS.
3. Replace title, kicker, dek, date, byline, essay body, prompt block(s). Each prompt
   goes in its OWN copy-block card. If the prompt boundary is ambiguous, STOP and ask —
   the prompt is the hero element; a mis-lift is the worst possible error.
4. Set `<link rel="canonical">` to `https://prompteddaily.com/<slug>/`.
5. Add a header image per VISUAL-SYSTEM.md at `/<slug>/header.png`, plus its
   `/img/<slug>.jpg` card thumbnail.
6. On `index.html`, point that card's `href` to `/<slug>/` and set the CTA to
   "Read + run the prompt".
7. Add "Also published on Medium" to the article footer if a Medium version exists.

## Visual system (summary — full spec in VISUAL-SYSTEM.md)
- Base: photorealistic, desaturated blue-grey monochrome. No warm sky.
- Amber is the only accent. Analytical mode = actuarial data overlay traced on
  machinery along a sightline, never on skin. Witness mode (loneliness, theology) =
  a single warm light source, no data grid.
- One human-scale figure inside a vast system. A ghosted "substrate beneath the
  surface." Wordmark bottom-left.
- Gemini renders the amber texture only; legible stats + wordmark are added in an
  overlay pass (Gemini garbles text).

## Design tokens (already in each page's CSS — match, don't reinvent)
- Colors: bg #16162b / #101024, ivory #ECE6D8, dim #8f8fa6, amber #E8A33D.
- Type: Fraunces (display/wordmark), IBM Plex Sans (UI), IBM Plex Mono (labels +
  prompt blocks), Newsreader (article body).

## What NOT to do
- No email-capture or subscribe UI. That model was deliberately rejected.
- No frameworks, build steps, or npm dependencies. Keep it static and hand-editable.
- No hotlinking Medium's CDN (miro.medium.com) for images. All images live in this repo.
- Don't reformat or "modernize" working pages you weren't asked to touch.
- Social links are Medium and X only (no dead placeholders).
