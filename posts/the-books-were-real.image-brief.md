# Image brief: "The Books Were Real. The Rarity Is Unproven."

Slug: `the-books-were-real`
Output targets: `/the-books-were-real/header.png` (16:9) and `/img/the-books-were-real.jpg` (640x360)

## Mode: Witness
The piece is a verification (Analytical) wrapped around a personal position on using a tool
you are uneasy about (Witness). The header carries the second half, because that is the part
a data grid would trivialize. Per VISUAL-SYSTEM.md, applying a data overlay to a Witness
piece is the failure mode: no grid, no ticks, no plot lines, no numeric glyphs.

## The four slots
- **Base scene:** a long reading table in a dark university or library room at night, one chair
  pulled back, one intact open book on the table.
- **What the amber is:** a single warm desk lamp falling across the open book and a small pool
  of the table. Nothing else is warm. Amber never touches the figure's skin or face.
- **Who the figure is:** a teacher or reader seen from behind, small against the room, standing
  at the table edge.
- **What the substrate is:** the hidden layer beneath the floor. A ghosted cross-section in cool
  blue-grey only: pallets of loose, unbound pages and the dark silhouette of a hydraulic cutting
  blade, faint, below the floorboards. No amber down there.

The contrast the image makes without words: one whole book in warm light above, the cut pages
beneath. Keep the substrate quiet. It should read on a second look, not the first.

## Gemini prompt (texture, not text)
> A quiet university reading room at night, photorealistic, desaturated cool blue-grey
> monochrome, wide establishing view with cinematic depth. One long wooden table, one chair
> pulled back, a single intact open book resting on the table. A lone teacher seen from behind,
> small against the room, standing at the table's edge. The only warm element in the entire
> frame is one amber desk lamp casting a soft pool of light across the open book and a small
> area of the tabletop; amber never touches the person's skin, hair, or face. Beneath the
> floorboards, a faint ghosted cross-section in pale blue-grey: stacked pallets of loose
> unbound pages and the dark outline of a hydraulic cutting blade, subtle and quiet, no amber
> in this lower layer. No grid, no tick marks, no plot lines. No text, letters, numbers,
> logos, or watermarks anywhere in the image. Stillness, restraint, human warmth. Economist
> precision with Foreign Affairs atmospheric weight. 16:9.

## After Gemini
1. Save the render somewhere outside the repo (Downloads is fine; the `_Sorter` automation may
   rename it, so check `ls -lat ~/Downloads`).
2. Run the overlay pass, which adds the wordmark bottom-left and writes both outputs:
   `python3 tools/make_images.py the-books-were-real <path-to-render>`
3. Add `hero_image` to `posts/the-books-were-real.json` using the alt and caption drafted below,
   set `card_thumb_alt`, rerun `tools/build_essay.py`, and review.

## Alt text and caption (drafts, for approval)
- alt: "A lone teacher at a long reading table at night, one amber lamp lighting an open book, and
  a faint ghosted outline of stacked loose pages and a cutting blade beneath the floor."
- caption: "One whole book above the floor, cut pages beneath it. Illustration generated with Gemini."
- card thumb alt: "A teacher at a reading table beside an amber lamp and open book, with ghosted stacks of
  loose pages beneath the floor."
