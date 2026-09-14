#!/usr/bin/env python3
"""Round 4 - "My name is 'bronier', it's logical the slats to be on the 'o'
letter." He is right, and my two earlier attempts were not good enough rather
than the idea being wrong. Four different ways of putting the slats ON the o.

What failed before, so it is not repeated:
  * slats cut clean through the ring  -> the o falls into four loose arcs;
  * slats floating inside the counter -> two bars in a circle read as a face.

The common fault was that the slats never TOUCHED the ring. Fluting that meets
the frame reads as a fluted panel; fluting that hovers inside it reads as eyes.
Three of the four below connect. The fourth solves it the other way, by making
the o heavy enough that cutting it cannot break it.

    python3 logo4.py
"""
from __future__ import annotations

import pathlib
import sys

import logo as L
from logo import text_path

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out4"
L.FONTS.setdefault("jost", "/home/freelancer5/.local/share/fonts/JostStatic-Light.ttf")

WORD = "bronier"
SIZE = 130.0
TRACK = 0.05
CLAY = "#a8503a"
INKBLACK = "#141414"
PAPER = "#ffffff"          # he asked for the site to go white; the sheet follows

# Jost Light, measured, /1000: o outer 39..511 x -10..470, counter 92..458 x
# 39..421, advance 550.
O_ADV, O_CX, O_CY, O_R, O_STEM = 0.550, 0.275, 0.230, 0.2095, 0.053


def _svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" '
            f'height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">'
            f'<defs>{defs}</defs>{body}</svg>')


def _paper(w, h, paper):
    return "" if paper is None else f'<rect width="{w:.0f}" height="{h:.0f}" fill="{paper}"/>'


def _layout(size, track):
    """The word with the o left out, and where the o would have gone."""
    paths, ox, x = [], None, 0.0
    for ch in WORD:
        if ch == "o" and ox is None:
            ox = x
            x += O_ADV * size + track * size
            continue
        d, w = text_path(ch, "jost", size, x, 0, 0)
        paths.append(d)
        x += w + track * size
    return "".join(paths), ox, x - track * size


def _word(paths, base_y, ink, pad):
    return (f'<g fill="{ink}" transform="translate({pad:.2f} {base_y:.2f})">'
            + paths + "</g>")


def _frame(size, track, ink, paper, o_body, defs="", extra_h=1.9):
    paths, ox, w = _layout(size, track)
    pad = size * 0.5
    W, H = w + pad * 2, size * extra_h
    base_y = H * 0.66
    cx, cy = pad + ox + O_CX * size, base_y - O_CY * size
    return (_svg(W, H, _paper(W, H, paper) + _word(paths, base_y, ink, pad)
                 + o_body(cx, cy), defs), W, H)


# --------------------------------------------------------------- the four o's
def o_connected(ink, accent, paper, size=SIZE, track=TRACK, n=4):
    """A - fluting that MEETS the ring.

    The bars run the full inside height and land on the stroke top and bottom,
    so the o reads as a length of fluted panel seen end-on. This is the one the
    earlier attempt should have been: the bars were deliberately kept clear of
    the stroke, and that gap is exactly what made it a face.
    """
    r, stem = O_R * size, O_STEM * size

    def body(cx, cy):
        inner = r - stem / 2
        bw = stem * 0.55
        pitch = (inner * 2 - bw) / (n + 1)
        out = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" '
               f'stroke="{ink}" stroke-width="{stem:.2f}"/>']
        for i in range(n):
            bx = cx - inner + pitch * (i + 1) - bw / 2
            # chord half-height at this x, so each bar stops ON the circle
            dx = abs(bx + bw / 2 - cx)
            half = max(0.0, (inner ** 2 - dx ** 2)) ** 0.5
            out.append(f'<rect x="{bx:.2f}" y="{cy - half:.2f}" width="{bw:.2f}" '
                       f'height="{half * 2:.2f}" fill="{ink}"/>')
        return "".join(out)
    return _frame(size, track, ink, paper, body)


def o_disc(ink, accent, paper, size=SIZE, track=TRACK, n=6):
    """B - the o becomes a solid disc of slats.

    No ring at all: the letter is a round piece of fluted panel. The most
    literal of the four and the one that survives smallest, because it is a
    filled shape rather than a thin outline.
    """
    r = O_R * size + O_STEM * size / 2

    def body(cx, cy):
        bw = (r * 2) / (n + (n - 1) * 0.32)
        gap = bw * 0.32
        out = [f'<clipPath id="disc"><circle cx="{cx:.2f}" cy="{cy:.2f}" '
               f'r="{r:.2f}"/></clipPath>', f'<g clip-path="url(#disc)">']
        for i in range(n):
            bx = cx - r + i * (bw + gap)
            out.append(f'<rect x="{bx:.2f}" y="{cy - r - 2:.2f}" width="{bw:.2f}" '
                       f'height="{r * 2 + 4:.2f}" fill="{accent if i == n // 2 else ink}"/>')
        out.append("</g>")
        return "".join(out)
    return _frame(size, track, ink, paper, body)


def o_heavy(ink, accent, paper, size=SIZE, track=TRACK, n=3):
    """C - a heavier o, cut through.

    Cutting the ring is what broke the letter last time. It breaks because the
    stroke is hairline. At 2.4x the weight the arcs are substantial enough to
    stay one letter, and the cuts read as the gaps between boards.
    """
    r = O_R * size
    stem = O_STEM * size * 2.4

    def body(cx, cy):
        groove = stem * 0.30
        span = r * 2 + stem
        gxs = sorted((cx + (i - (n - 1) / 2) * (span / (n + 1)) - groove / 2, groove)
                     for i in range(n))
        bands, x0 = [], cx - span
        for gx, gw in gxs:
            if gx > x0:
                bands.append((x0, gx - x0))
            x0 = gx + gw
        bands.append((x0, cx + span - x0))
        clip = '<clipPath id="hv">' + "".join(
            f'<rect x="{bx:.2f}" y="{cy - span:.2f}" width="{bw:.2f}" '
            f'height="{span * 2:.2f}"/>' for bx, bw in bands) + "</clipPath>"
        return (clip + f'<g clip-path="url(#hv)"><circle cx="{cx:.2f}" cy="{cy:.2f}" '
                f'r="{r:.2f}" fill="none" stroke="{ink}" stroke-width="{stem:.2f}"/></g>')
    return _frame(size, track, ink, paper, body)


def o_halfflute(ink, accent, paper, size=SIZE, track=TRACK, n=3):
    """D - fluting in the lower half only.

    The top of the o stays a clean unbroken curve, which is what the eye uses
    to read the letter, and the fluting fills the bottom the way a panel sits
    on a floor. Quieter than A, less literal than B.
    """
    r, stem = O_R * size, O_STEM * size

    def body(cx, cy):
        inner = r - stem / 2
        bw = stem * 0.55
        pitch = (inner * 2 - bw) / (n + 1)
        out = [f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" '
               f'stroke="{ink}" stroke-width="{stem:.2f}"/>']
        for i in range(n):
            bx = cx - inner + pitch * (i + 1) - bw / 2
            dx = abs(bx + bw / 2 - cx)
            half = max(0.0, (inner ** 2 - dx ** 2)) ** 0.5
            out.append(f'<rect x="{bx:.2f}" y="{cy:.2f}" width="{bw:.2f}" '
                       f'height="{half:.2f}" fill="{ink}"/>')
        return "".join(out)
    return _frame(size, track, ink, paper, body)


VARIANTS = {"connected": o_connected, "disc": o_disc, "heavy": o_heavy,
            "half": o_halfflute}
LABEL = {"connected": "A - fluting meets the ring", "disc": "B - solid fluted disc",
         "heavy": "C - heavier o, cut through", "half": "D - fluted lower half"}


def main() -> None:
    import cairosvg
    want = sys.argv[1:] or list(VARIANTS)
    OUT.mkdir(parents=True, exist_ok=True)
    for k in want:
        fn = VARIANTS[k]
        for tag, ink, accent, paper in (("clay", CLAY, CLAY, PAPER),
                                        ("black", INKBLACK, INKBLACK, PAPER),
                                        ("reversed", "#ffffff", "#ffffff", "#24211f")):
            svg, w, h = fn(ink, accent, paper)
            b = OUT / f"{k}-{tag}"
            b.with_suffix(".svg").write_text(svg, encoding="utf-8")
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(b) + ".png",
                             output_width=int(w * 2), output_height=int(h * 2))
            tsvg, tw, th = fn(ink, accent, None)
            tb = OUT / f"{k}-{tag}-transparent"
            tb.with_suffix(".svg").write_text(tsvg, encoding="utf-8")
            cairosvg.svg2png(bytestring=tsvg.encode(), write_to=str(tb) + ".png",
                             output_width=int(tw * 2), output_height=int(th * 2))
        print(f"{k:<10} {LABEL[k]}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
