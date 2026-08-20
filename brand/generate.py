"""
Generator for the offset mark.

The mark is defined once, here, in grid units (u). Every asset in this
repo is emitted from this file. Do not hand-edit the SVGs -- change the
constants below and re-run:

    python3 generate.py

Geometry
--------
Body          12u x 12u square
Cut           horizontal, 5u from the top (a 5:7 division)
Displacement  upper mass moved 2u to the right (one sixth of the body)
Bounding box  14u x 12u  (7:6)
Corners       sharp, no radius, no optical correction
"""

import os
from PIL import Image, ImageDraw

W_U, H_U = 14, 12          # bounding box in units
BODY_U = 12                # square body
CUT_U = 5                  # cut distance from top
SHIFT_U = 2                # horizontal displacement
CLEARSPACE_U = 2           # minimum breathing room
ICON_CANVAS_U = 20         # app icon canvas (mark height 12u inside 20u)

INK = "#111111"
PAPER = "#FFFFFF"
GHOST = "#C4C4C4"

OUT = os.path.dirname(os.path.abspath(__file__))


def blocks(ox=0, oy=0, u=1):
    """Return the two rectangles (x0, y0, x1, y1) that compose the mark."""
    upper = (ox + SHIFT_U * u, oy, ox + (SHIFT_U + BODY_U) * u, oy + CUT_U * u)
    lower = (ox, oy + CUT_U * u, ox + BODY_U * u, oy + H_U * u)
    return upper, lower


def outline(ox=0, oy=0, u=1):
    """Return the mark as a single 8-point polygon."""
    x, y = ox, oy
    return [
        (x + SHIFT_U * u, y),
        (x + W_U * u, y),
        (x + W_U * u, y + CUT_U * u),
        (x + BODY_U * u, y + CUT_U * u),
        (x + BODY_U * u, y + H_U * u),
        (x, y + H_U * u),
        (x, y + CUT_U * u),
        (x + SHIFT_U * u, y + CUT_U * u),
    ]


def points_attr(pts):
    return " ".join(f"{x:g},{y:g}" for x, y in pts)


def svg(view_w, view_h, body, title, desc):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" '
        f'width="{view_w * 16}" height="{view_h * 16}" role="img" '
        f'aria-labelledby="t d" fill="none">\n'
        f'  <title id="t">{title}</title>\n'
        f'  <desc id="d">{desc}</desc>\n'
        f"{body}"
        f"</svg>\n"
    )


DESC = (
    "A square cut horizontally five units from the top, with the upper mass "
    "displaced two units to the right."
)


def write(name, text):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(text)
    print("wrote", name)


# ---------------------------------------------------------------- SVG assets

poly = points_attr(outline())

write(
    "logo.svg",
    svg(W_U, H_U,
        f'  <polygon points="{poly}" fill="currentColor"/>\n',
        "Offset mark", DESC),
)

write(
    "logo-black.svg",
    svg(W_U, H_U,
        f'  <polygon points="{poly}" fill="{INK}"/>\n',
        "Offset mark, black", DESC),
)

write(
    "logo-white.svg",
    svg(W_U, H_U,
        f'  <polygon points="{poly}" fill="{PAPER}"/>\n',
        "Offset mark, white", DESC),
)

write(
    "logo-ghost.svg",
    svg(W_U, H_U,
        f'  <rect x="0" y="0" width="{BODY_U}" height="{CUT_U}" '
        f'fill="none" stroke="{GHOST}" stroke-width="0.08"/>\n'
        f'  <polygon points="{poly}" fill="currentColor"/>\n',
        "Offset mark, ghost variant",
        DESC + " A hairline outline shows the upper mass in its original position."),
)

cs = CLEARSPACE_U
write(
    "logo-clearspace.svg",
    svg(W_U + cs * 2, H_U + cs * 2,
        f'  <polygon points="{points_attr(outline(cs, cs))}" fill="currentColor"/>\n',
        "Offset mark with clearspace",
        DESC + f" Padded by {cs} grid units on every side."),
)

ic = ICON_CANVAS_U
ox, oy = (ic - W_U) / 2, (ic - H_U) / 2
write(
    "app-icon.svg",
    svg(ic, ic,
        f'  <rect width="{ic}" height="{ic}" fill="{PAPER}"/>\n'
        f'  <polygon points="{points_attr(outline(ox, oy))}" fill="{INK}"/>\n',
        "Offset mark app icon",
        DESC + f" Centred on a {ic} unit square canvas."),
)

write(
    "app-icon-dark.svg",
    svg(ic, ic,
        f'  <rect width="{ic}" height="{ic}" fill="{INK}"/>\n'
        f'  <polygon points="{points_attr(outline(ox, oy))}" fill="{PAPER}"/>\n',
        "Offset mark app icon, reversed",
        DESC + f" White on black, centred on a {ic} unit square canvas."),
)


# --------------------------------------------------------------- PNG rasters
# Every raster is composed from two whole-pixel rectangles rather than
# rasterised from the SVG. Edges therefore land exactly on pixel boundaries
# and nothing is softened by antialiasing -- which is what keeps the 5:7 cut
# and the 2u displacement legible at 16px.

MASKABLE_CANVAS_U = 26   # extra padding so nothing is lost to platform cropping

count = 0


def png(rel, w, h, u, ink, bg=None):
    """Draw the mark at unit size u, centred on a w x h canvas."""
    global count
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new("RGBA", (w, h), bg if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ox = round((w - W_U * u) / 2)
    oy = round((h - H_U * u) / 2)
    for x0, y0, x1, y1 in blocks(ox, oy, u):
        d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=ink)
    if bg:
        img = img.convert("RGB")
    img.save(path)
    count += 1
    print(f"  {rel:<44} {w}x{h}  u={u}")


def fit(size, canvas_u):
    """Largest whole-pixel unit that fits the mark in a canvas of canvas_u."""
    return max(1, size // canvas_u)


# --- Transparent mark, tight bounding box. Docs, slides, README, overlays.
print("\nmark (transparent)")
for size in (16, 32, 48, 64, 128, 256, 512, 1024, 2048):
    u = fit(size, W_U)
    png(f"png/mark/mark-{size}.png", size, size, u, INK)
    png(f"png/mark/mark-{size}-white.png", size, size, u, PAPER)

# --- Favicons. Same tight fit; duplicated under a predictable name.
print("\nfavicons")
for size in (16, 32, 48, 64):
    png(f"favicon-{size}.png", size, size, fit(size, W_U), INK)

# --- App icons. The 20u canvas rule, so clearspace is preserved.
print("\napp icons")
for size in (128, 180, 192, 256, 512, 1024):
    u = fit(size, ICON_CANVAS_U)
    png(f"png/icon/icon-{size}.png", size, size, u, INK, PAPER)
    png(f"png/icon/icon-{size}-dark.png", size, size, u, PAPER, INK)

# --- Apple touch icon. Opaque, no alpha, iOS adds its own corner radius.
print("\napple touch")
png("apple-touch-icon.png", 180, 180, fit(180, ICON_CANVAS_U), INK, PAPER)

# --- Maskable icons. Wider canvas so platform cropping cannot clip the mark.
print("\nmaskable (safe-zone padded)")
for size in (192, 512):
    u = fit(size, MASKABLE_CANVAS_U)
    png(f"png/maskable/maskable-{size}.png", size, size, u, INK, PAPER)
    png(f"png/maskable/maskable-{size}-dark.png", size, size, u, PAPER, INK)

# --- Social cards. Open Graph and GitHub repository preview.
print("\nsocial")
for name, w, h in (("og-1200x630", 1200, 630), ("github-1280x640", 1280, 640)):
    u = h // 20
    png(f"png/social/{name}.png", w, h, u, INK, PAPER)
    png(f"png/social/{name}-dark.png", w, h, u, PAPER, INK)

# --- Multi-resolution .ico for legacy browsers.
Image.open(os.path.join(OUT, "favicon-64.png")).save(
    os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
)
count += 1
print(f"\n  favicon.ico (16/32/48/64)")
print(f"\n{count} raster files")
