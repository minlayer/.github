# Brand

The mark is a square, cut once off-centre, with the upper mass displaced
sideways. Nothing is removed — the form stays whole. It reads as a shift, a
diff, a version of the thing that was there.

## Geometry

Everything derives from one grid unit, `u`. Nothing here is eyeballed.

| Property | Value |
| --- | --- |
| Body | `12u × 12u` square |
| Cut | horizontal, `5u` from the top (a 5:7 division) |
| Displacement | `2u` right — one sixth of the body width |
| Bounding box | `14u × 12u` (7:6) |
| Corners | sharp; no radius, no optical correction |
| Clearspace | `2u` on all sides, minimum |
| App icon | mark height `12u`, centred on a `20u` square canvas |

The cut is deliberately not at the halfway point and the displacement is
deliberately not a round fraction of the height. Those two ratios are what
separate this from a generic stagger. Quote them if the mark is ever
questioned.

## Files

### Vector

| File | Use |
| --- | --- |
| `logo.svg` | primary; fills with `currentColor`, so it inherits from CSS |
| `logo-black.svg` / `logo-white.svg` | fixed-colour, for contexts without CSS |
| `logo-ghost.svg` | large-format and docs headers only (see below) |
| `logo-clearspace.svg` | placement reference, showing the `2u` margin |
| `app-icon.svg` / `app-icon-dark.svg` | square-canvas lockups |

Prefer the SVGs everywhere they work. The rasters exist for the places that
refuse vector: browser chrome, OS icon slots, and social card scrapers.

### Raster

| Path | Sizes | Notes |
| --- | --- | --- |
| `favicon-*.png`, `favicon.ico` | 16, 32, 48, 64 | transparent; `.ico` bundles all four |
| `apple-touch-icon.png` | 180 | opaque, no alpha — iOS requires this |
| `png/mark/mark-*.png` | 16 → 2048 | transparent, tight crop, black and white |
| `png/icon/icon-*.png` | 128 → 1024 | `20u` canvas, light and dark |
| `png/maskable/maskable-*.png` | 192, 512 | `26u` canvas for PWA safe-zone cropping |
| `png/social/*.png` | 1200×630, 1280×640 | Open Graph and GitHub preview |

Every raster is composed from whole-pixel rectangles rather than rasterised
from the SVG, so no edge is antialiased. Each file contains exactly two
colours. This is what keeps the 5:7 cut and the `2u` displacement readable at
16px, where a rendered SVG would turn to grey mush.

`generate.py` is the source of truth. All 44 rasters and all 7 vectors are
emitted from it.

## Colour

Black `#111111`, white `#FFFFFF`, and one grey `#C4C4C4`.

The grey has exactly one job: the ghost outline. It never appears inside the
mark itself. If grey creeps into the form, the mark stops being minimal and
starts being a design.

## The ghost variant

`logo-ghost.svg` shows where the upper mass used to be, as a hairline. It is a
second state, not a second logo — use it for large-format placements, docs
headers, and loading states. Never below 64px, where the hairline disappears.

## Rules

- No container. Resist the rounded square; the mark sits directly on its
  surface.
- No radius, ever. The sharp corners are the mark.
- One lockup arrangement only, if you add a wordmark. Two lockups is one too
  many.
- Do not rescale a PNG. Re-run `generate.py` at the size you need.
- Do not hand-edit the SVGs. Change the constants in `generate.py` and rebuild.

## Known risk

At very small sizes with heavy antialiasing, the mark can read as a bold
letterform — roughly an `S` or `Z`. The supplied PNGs are drawn as whole-pixel
rectangles rather than rasterised from SVG, which avoids this. If you generate
your own small sizes by another route, check the result reversed
(white on black) before shipping it.

This has not been cleared against any trademark register. Before filing
anything, run `logo.svg` through the WIPO Global Brand Database image search
under Vienna Classification 26.04 (quadrilaterals) and talk to an attorney.
