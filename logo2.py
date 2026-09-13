#!/usr/bin/env python3
"""Round 2 - his brief, verbatim: "Something else, doesn't need to be brown
color. Only Bronier. Without decor."

So three things change from round one:
  * DECOR is gone. The logo is the word BRONIER and nothing else, which makes
    this a wordmark exercise rather than a symbol-plus-name one;
  * the brown is off the table. Each direction gets its own palette;
  * no reruns of round one - no fluted tiles, no arch, no rounded-square badge.

One thing worth him knowing rather than me quietly deciding: his SITE is brown.
A charcoal or black wordmark drops onto the current site untouched. A green or
a clay one means the site accent moves with it. That is a real consequence of
"doesn't need to be brown" and it is his call, so every direction is also drawn
in plain ink so he can judge the SHAPE with the colour argument set aside.

    python3 logo2.py          # all five, every colourway
    python3 logo2.py fluted
"""
from __future__ import annotations

import math
import pathlib
import sys

from logo import text_path, text_width, _font  # noqa: F401  (shared machinery)

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out2"

# Round-one fonts plus a serif and a geometric, all licensed for commercial use:
# Lato and Jost are SIL OFL; Latin Modern is the GUST Font License.
import logo as L
L.FONTS.update({
    "hair": "/usr/share/fonts/truetype/lato/Lato-Hairline.ttf",
    "thin": "/usr/share/fonts/truetype/lato/Lato-Thin.ttf",
    "semibold": "/usr/share/fonts/truetype/lato/Lato-Semibold.ttf",
    "serif": "/usr/share/texmf/fonts/opentype/public/lm/lmroman10-bold.otf",
    "jost": "/home/freelancer5/.local/share/fonts/JostStatic-Light.ttf",
    "jostxl": "/home/freelancer5/.local/share/fonts/JostStatic-ExtraLight.ttf",
})

WORD = "BRONIER"

#: ink, accent, paper. No browns. "neutral" is the same shape in plain ink and
#: is generated for every direction, so colour and form can be judged apart.
PALETTES = {
    "fluted":  dict(name="charcoal + amber", ink="#1d1d1b", accent="#d98324", paper="#f4f1ec"),
    "hairline": dict(name="ink on white",     ink="#141414", accent="#141414", paper="#ffffff"),
    "serif":   dict(name="deep green",        ink="#1f3d33", accent="#c9a227", paper="#f3f1ea"),
    "framed":  dict(name="slate blue",        ink="#2b3a45", accent="#7a9aa8", paper="#f2f4f5"),
    "lower":   dict(name="clay",              ink="#a8503a", accent="#a8503a", paper="#faf5f0"),
}
NEUTRAL = dict(name="plain ink", ink="#141414", accent="#141414", paper="#ffffff")
REVERSED = {                       # the same mark on its own dark ground
    "fluted":  "#1d1d1b", "hairline": "#141414", "serif": "#1f3d33",
    "framed":  "#2b3a45", "lower": "#a8503a",
}


def _svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" '
            f'height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">'
            f'<defs>{defs}</defs>{body}</svg>')


def _paper(w, h, paper):
    return "" if paper is None else f'<rect width="{w:.0f}" height="{h:.0f}" fill="{paper}"/>'


# ---------------------------------------------------------------- directions
def d_fluted(ink, accent, paper, size=120.0, track=0.16):
    """BRONIER with the O drawn as a fluted ring.

    The panels are vertical fluting; putting it inside the O keeps the product
    in the logo without a separate symbol to place, which is the whole point
    now that DECOR is gone. The ring is drawn rather than typed so its weight
    can be matched to Lato Black's stem instead of hoping a circle glyph fits.
    """
    # MEASURED off Lato-Black's own O rather than eyeballed. First attempt used
    # round numbers and a tracking gap either side of the ring: the O came out
    # smaller than its neighbours, sat low, and floated away from the R. These
    # are the glyph's real metrics at upem 2000 - outer 57..1571, counter
    # 403..1225, y -16..1473, advance 1629 - divided through by 2000.
    O_ADV = 0.8145 * size          # advance width, so spacing matches the font
    O_CX = 0.4070 * size           # ink centre from the pen origin
    O_CY = 0.3643 * size           # ink centre above the baseline
    O_R = 0.2920 * size            # mid-stroke radius
    O_STEM = 0.1730 * size         # stroke weight = (outer - counter) / 2

    w_pre = text_width("BR", "black", size, track)
    w_post = text_width("NIER", "black", size, track)
    pad = size * 0.5
    W = pad * 2 + w_pre + track * size + O_ADV + track * size + w_post
    H = size * 2.1
    base_y = H * 0.66
    ring_x = pad + w_pre + track * size
    cx, cy = ring_x + O_CX, base_y - O_CY

    pre_d, _ = text_path("BR", "black", size, pad, base_y, track)
    post_d, _ = text_path("NIER", "black", size,
                          ring_x + O_ADV + track * size, base_y, track)
    # Three grooves across the ring. Two read as a broken O, four close it up.
    # The middle one is the accent - a coloured groove belongs to the idea,
    # where the arc of colour the first version drew just looked like a fault.
    groove = O_STEM * 0.40
    span = O_R * 2 + O_STEM

    def gx(i):
        return cx - span / 2 + (i + 1) * (span / 4) - groove / 2

    # The grooves are a MASK, not bars painted in the paper colour. Painting
    # them only works while there is a paper colour to paint - on the
    # transparent asset, which is the file that actually gets used, white bars
    # would have appeared across the O on every dark background.
    mask = ("".join(
        f'<rect x="{gx(i):.2f}" y="{cy - span / 2 - 2:.2f}" width="{groove:.2f}" '
        f'height="{span + 4:.2f}" fill="#000"/>' for i in range(3)))
    defs = (f'<mask id="oflute"><rect width="{W:.0f}" height="{H:.0f}" fill="#fff"/>'
            f'{mask}</mask>'
            f'<clipPath id="oaccent"><rect x="{gx(1):.2f}" '
            f'y="{cy - span / 2 - 2:.2f}" width="{groove:.2f}" '
            f'height="{span + 4:.2f}"/></clipPath>')
    ring = (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{O_R:.2f}" fill="none" '
            f'stroke="{ink}" stroke-width="{O_STEM:.2f}"/>')
    # the accent is the same ring drawn again, showing only inside the middle
    # groove's column - so the colour sits ON the stroke rather than beside it
    accent_ring = (f'<g clip-path="url(#oaccent)"><circle cx="{cx:.2f}" cy="{cy:.2f}" '
                   f'r="{O_R:.2f}" fill="none" stroke="{accent}" '
                   f'stroke-width="{O_STEM:.2f}"/></g>')
    body = (_paper(W, H, paper)
            + f'<g fill="{ink}">{pre_d}{post_d}</g>'
            + f'<g mask="url(#oflute)">{ring}</g>'
            + accent_ring)
    return _svg(W, H, body, defs), W, H


def d_hairline(ink, accent, paper, size=112.0, track=0.46):
    """Very light, very open, sitting on a rule that runs past the word.

    The opposite bet to a heavy mark: at large sizes it reads as a gallery or
    an architecture practice. It is also the most fragile of the five - below
    about 30px the hairline strokes start to disappear, and that is said out
    loud on the sheet rather than discovered by him later.
    """
    w = text_width(WORD, "thin", size, track)
    pad = size * 0.62
    W, H = w + pad * 2, size * 2.25
    base = H * 0.56
    d, _ = text_path(WORD, "thin", size, pad, base, track)
    rule_y = base + size * 0.42
    body = (_paper(W, H, paper)
            + f'<g fill="{ink}">{d}</g>'
            + f'<rect x="{pad * 0.45:.2f}" y="{rule_y:.2f}" '
              f'width="{W - pad * 0.9:.2f}" height="{size * 0.018:.2f}" fill="{accent}"/>')
    return _svg(W, H, body), W, H


def d_serif(ink, accent, paper, size=116.0, track=0.19):
    """A serif, for the part of the market that buys panels for a living room
    rather than a terrace. Latin Modern Roman Bold - a Computer Modern cut, so
    the contrast is high without tipping into a fashion-house didone, which is
    what his current logo already is and what he asked to move away from."""
    w = text_width(WORD, "serif", size, track)
    pad = size * 0.6
    W, H = w + pad * 2, size * 2.0
    base = H * 0.62
    d, _ = text_path(WORD, "serif", size, pad, base, track)
    body = _paper(W, H, paper) + f'<g fill="{ink}">{d}</g>' 
    return _svg(W, H, body), W, H


def d_framed(ink, accent, paper, size=86.0, track=0.34):
    """The word inside a thin rectangle. The frame IS the panel - a reference
    with no fluting in it, which keeps it clear of round one."""
    w = text_width(WORD, "semibold", size, track)
    padx, pady = size * 0.95, size * 0.78
    W, H = w + padx * 2, size * 2.6
    base = H * 0.60
    d, _ = text_path(WORD, "semibold", size, padx, base, track)
    lw = size * 0.045
    inset = size * 0.30
    body = (_paper(W, H, paper)
            + f'<rect x="{inset:.2f}" y="{inset:.2f}" width="{W - inset * 2:.2f}" '
              f'height="{H - inset * 2:.2f}" fill="none" stroke="{ink}" '
              f'stroke-width="{lw:.2f}"/>'
            + f'<g fill="{ink}">{d}</g>')
    return _svg(W, H, body), W, H


def d_lower(ink, accent, paper, size=130.0, track=0.05):
    """Lowercase, geometric, light. The most contemporary of the five and the
    only one that does not shout. Jost Light - a Futura cut, SIL OFL."""
    word = "bronier"
    w = text_width(word, "jost", size, track)
    pad = size * 0.5
    W, H = w + pad * 2, size * 1.9
    base = H * 0.66
    d, _ = text_path(word, "jost", size, pad, base, track)
    body = (_paper(W, H, paper) + f'<g fill="{ink}">{d}</g>')
    return _svg(W, H, body), W, H


DIRECTIONS = {"fluted": d_fluted, "hairline": d_hairline, "serif": d_serif,
              "framed": d_framed, "lower": d_lower}


# -------------------------------------------------------------------- icons
def icon(kind, ink, accent, paper, size=512.0):
    """The square icon. He wants only the word, so the icon is the word's own
    first letter in the same treatment - not a new symbol smuggled in."""
    if kind == "lower":
        d, w = text_path("b", "jost", size * 0.62, 0, size * 0.72)
    elif kind == "serif":
        d, w = text_path("B", "serif", size * 0.60, 0, size * 0.72)
    elif kind == "hairline":
        d, w = text_path("B", "thin", size * 0.62, 0, size * 0.70)
    else:
        d, w = text_path("B", "black", size * 0.58, 0, size * 0.70)
    body = (f'<rect width="{size:.0f}" height="{size:.0f}" rx="{size * 0.19:.0f}" '
            f'fill="{ink}"/>'
            f'<g fill="{paper}" transform="translate({(size - w) / 2:.2f} 0)">{d}</g>')
    if kind != "lower":
        body += (f'<rect x="{size * 0.33:.0f}" y="{size * 0.775:.0f}" '
                 f'width="{size * 0.34:.0f}" height="{size * 0.038:.0f}" '
                 f'fill="{accent}"/>')
    return _svg(size, size, body)


def main() -> None:
    import cairosvg
    want = sys.argv[1:] or list(DIRECTIONS)
    OUT.mkdir(parents=True, exist_ok=True)
    for k in want:
        if k not in DIRECTIONS:
            raise SystemExit(f"unknown direction {k}; have {list(DIRECTIONS)}")
        fn = DIRECTIONS[k]
        pal = PALETTES[k]
        jobs = [("colour", pal["ink"], pal["accent"], pal["paper"]),
                ("neutral", NEUTRAL["ink"], NEUTRAL["accent"], NEUTRAL["paper"]),
                ("reversed", pal["paper"], pal["accent"], REVERSED[k])]
        for tag, ink, accent, paper in jobs:
            svg, w, h = fn(ink, accent, paper)
            b = OUT / f"{k}-{tag}"
            b.with_suffix(".svg").write_text(svg, encoding="utf-8")
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(b) + ".png",
                             output_width=int(w * 2), output_height=int(h * 2))
            # and the same thing with no paper at all - the delivered asset
            tsvg, tw, th = fn(ink, accent, None)
            tb = OUT / f"{k}-{tag}-transparent"
            tb.with_suffix(".svg").write_text(tsvg, encoding="utf-8")
            cairosvg.svg2png(bytestring=tsvg.encode(), write_to=str(tb) + ".png",
                             output_width=int(tw * 2), output_height=int(th * 2))
        isvg = icon(k, pal["ink"], pal["accent"], pal["paper"])
        ib = OUT / f"{k}-icon"
        ib.with_suffix(".svg").write_text(isvg, encoding="utf-8")
        cairosvg.svg2png(bytestring=isvg.encode(), write_to=str(ib) + ".png",
                         output_width=512, output_height=512)
        print(f"{k:<9} {pal['name']}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
