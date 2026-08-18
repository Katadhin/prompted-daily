# Prompted.daily — Visual identity system

One grammar, many subjects. Keep the *rules* constant so every header reads as Prompted;
swap the *slots* so no two pieces look alike.

## Two modes (same skeleton, different amber)
- **Analytical** — geopolitics, macro, regional, commerce. Amber behaves as an *actuarial
  data overlay*: grid, tick marks, plot lines, abstract numeric glyphs traced onto the
  machinery/terrain along a sightline.
- **Witness** — loneliness, theology, the personal register. Amber behaves as a *single
  warm light source* (a lamp, a screen glow, a candle). No grid, no ticks. Same monochrome
  and lone figure; the accent becomes a hearth, not a spreadsheet.

Applying the data overlay to a Witness piece is the failure mode. Match the mode to the register.

## Invariants (true in every header)
1. Photorealistic or institutional base, desaturated to a cool **blue-grey monochrome**.
   No warm sky, no golden hour.
2. **Amber is the only accent color.** In Analytical mode it traces machinery/terrain along
   the figure's sightline. It **never touches human skin or face** — surveillance read.
3. **One human-scale subject** inside a vast system, small against it, usually back-to-camera.
4. A **ghosted "substrate beneath the surface"** — the hidden layer under the visible one.
5. Wide aerial/establishing or institutional vantage; cinematic depth. **Wordmark bottom-left.**

## Variable slots (fill these per piece)
- **Base scene** — the subject's world (the valley, the strait, the trading floor, the room).
- **What the amber traces / is** — the domain's data layer (Analytical) or its warm source (Witness).
- **Who the figure is** — worker, analyst, official, resident, reader, believer.
- **What the substrate is** — the hidden system relevant to this topic.

## Production rules
- **Gemini gets texture, not text.** It garbles numbers and words. Prompt only for the amber
  *pattern*; add legible stats and the **Prompted.daily** wordmark in the Canva/Figma overlay pass.
- Export 16:9. Keep a per-piece `header.png` co-located with the article (`<slug>/header.png`),
  wired to `og:image`.

## Lane seed prompts (starting points — adjust the base scene per piece)

**Geopolitics** (Analytical; the literal submarine lives here)
> Aerial view of a narrow maritime strait at dawn, photorealistic, desaturated blue-grey
> monochrome, a single cargo tanker transiting the center channel. A thin amber actuarial
> overlay of chokepoint-risk ticks, shipping-volume plot lines, and abstract numeric glyphs
> projected across the water's surface along a sightline. A lone naval officer in silhouette
> on a foreground vantage, small against the scene; amber never touches his skin. A ghosted
> submarine and an undersea cable run beneath the surface in the lower frame. Amber the only
> accent, no warm sky. Economist precision, Foreign Affairs weight. 16:9.

**Macro / markets** (Analytical)
> Institutional interior of a central-bank hall or trading floor, photorealistic, desaturated
> blue-grey monochrome, vast and echoing. A single figure dwarfed by the architecture and dark
> screens. A thin amber overlay of yield-curve lines, rate-probability ticks, and abstract
> numeric glyphs traced across the screens and floor along the figure's sightline; amber never
> on skin. Beneath the floor, a ghosted x-ray of the financial system's plumbing — pipes,
> conduit, wiring. Amber the only accent, no warm light elsewhere. 16:9.

**Civic / cities** (Analytical)
> Aerial view of a dense rowhouse city grid at dusk, photorealistic, desaturated blue-grey
> monochrome. A thin amber overlay of civic-service ticks and coverage plot lines traced along
> the streets. A lone resident sweeping a stoop in the foreground, small against the grid; amber
> never on skin. Beneath the street, a ghosted x-ray of sewer, transit, and utility lines — the
> infrastructure under the neighborhood. Amber the only accent, no warm sky. 16:9.

**Witness / personal / theology** (Witness mode)
> A quiet interior at night, photorealistic, desaturated blue-grey monochrome — a single room,
> a table, a chair pulled back. One human figure alone, seen from behind or at a distance, small
> in the space. The only warm element is a single amber light source — a lamp or a screen glow —
> falling softly, never a data grid, never ticks. A faint ghosted presence beneath or beyond the
> room suggesting the unseen. Amber the only accent. Stillness, restraint, human warmth. 16:9.

---
This is the image half of the Prompted publish skill: given a piece's subject and lane, fill the
four slots, pick the mode, generate the base render in Gemini, then add wordmark + stats in overlay.
