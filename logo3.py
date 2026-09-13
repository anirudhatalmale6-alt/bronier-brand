#!/usr/bin/env python3
"""Round 3 - "Lowercase is good. Can you also try to create something related
to my niche. So Bronier but with something on my niche, so it can be niche
related."

So the base is settled: the lowercase Jost Light wordmark from round 2 (I),
in his clay colour. What changes is that each version now carries one piece of
the product - decorative wall panels, which are vertical fluted slats. Five
ways in, from the quietest to the most obvious.

The rule I am holding to: the niche cue has to come OUT of the word, not get
parked next to it. He asked twice for "only Bronier", and a wordmark with a
clip-art panel beside it is a wordmark with clip-art beside it.

Every shape here is drawn from Jost Light's OWN measured glyph metrics
(upem 1000): 'o' outer 39..511 x -10..470, counter 92..458 x 39..421, advance
550; 'i' tittle 79..153 x 631..705, stem 90..142, x-height 460, advance 232.
Round numbers are how the round-2 O came out smaller than its neighbours.

    python3 logo3.py            # all five
    python3 logo3.py slatdot
"""
from __future__ import annotations

import pathlib
import sys

import logo as L
from logo import text_path, text_width

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out3"
L.FONTS.setdefault("jost", "/home/freelancer5/.local/share/fonts/JostStatic-Light.ttf")

WORD = "bronier"
SIZE = 130.0
TRACK = 0.05

CLAY = "#a8503a"
INKBLACK = "#141414"
PAPER = "#faf5f0"

# --- Jost Light, measured, divided by upem 1000 --------------------------------
O_ADV, O_CX, O_CY, O_R, O_STEM = 0.550, 0.275, 0.230, 0.2095, 0.053
I_ADV, I_STEMW, I_STEMX = 0.232, 0.052, 0.116      # tittle centre x = 0.116 em
I_DOT_LO, I_DOT_HI = 0.631, 0.705                  # the dot it replaces
XH = 0.460


def _svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" '
            f'height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">'
            f'<defs>{defs}</defs>{body}</svg>')



def _keep_bands(x0, x1, y0, y1, grooves, cid):
    """A clipPath of everything EXCEPT the groove columns.

    Not a <mask>. cairosvg silently ignores <mask> - a positive control
    (black square, white stripe masked out) came back solid black, while the
    same test with clip-path came back correct. The grooves in round two's
    fluted O therefore never rendered in any PNG, and the PNG and the SVG of
    the same logo disagreed with each other. Bands it is.
    """
    rects, x = [], x0
    for gx, gw in sorted(grooves):
        if gx > x:
            rects.append((x, gx - x))
        x = max(x, gx + gw)
    if x < x1:
        rects.append((x, x1 - x))
    return ('<clipPath id="%s">' % cid) + "".join(
        f'<rect x="{rx:.2f}" y="{y0:.2f}" width="{rw:.2f}" height="{y1 - y0:.2f}"/>'
        for rx, rw in rects) + "</clipPath>"

def _paper(w, h, paper):
    return "" if paper is None else f'<rect width="{w:.0f}" height="{h:.0f}" fill="{paper}"/>'



def _counter_flutes(cx, cy, r, stem, ink, n=2):
    """Three short slats INSIDE the o's counter.

    Cutting grooves through the ring itself broke the letter into four
    disconnected arcs - the fluting won and the o lost. Putting the slats in
    the hole keeps the letter whole and still says panel. The bars stop short
    of the stroke so they never touch it, which is what would turn them back
    into a cut.
    """
    inner = r - stem / 2
    # Thinner and shorter than the first pass, which packed the counter solid
    # and turned the o into a coin. A slat is a line, not a block.
    bw = stem * 0.52
    pitch = inner * 0.78
    h = inner * 0.86
    out = []
    for i in range(n):
        bx = cx + (i - (n - 1) / 2) * pitch - bw / 2
        out.append(f'<rect x="{bx:.2f}" y="{cy - h / 2:.2f}" width="{bw:.2f}" '
                   f'height="{h:.2f}" rx="{bw / 2:.2f}" fill="{ink}"/>')
    return "".join(out)


def _pieces(size, track, dotless=False, skip_o=False):
    """Lay the word out letter by letter so a glyph can be swapped for a drawn
    shape without the spacing moving. Returns (paths, marks, width) where
    `marks` are (kind, pen_x) for whatever was left out."""
    paths, marks = [], []
    x = 0.0
    for ch in WORD:
        if ch == "i" and dotless:
            d, w = text_path("ı", "jost", size, x, 0, 0)   # dotless i
            paths.append((d, x))
            marks.append(("i", x))
            x += I_ADV * size + track * size
            continue
        if ch == "o" and skip_o:
            marks.append(("o", x))
            x += O_ADV * size + track * size
            continue
        d, w = text_path(ch, "jost", size, x, 0, 0)
        paths.append((d, x))
        x += w + track * size
    return paths, marks, x - track * size


def _draw(paths, base_y, ink):
    """text_path was asked for y=0; shift the whole lot onto the baseline."""
    return (f'<g fill="{ink}" transform="translate(0 {base_y:.2f})">'
            + "".join(d for d, _ in paths) + "</g>")


# ------------------------------------------------------------------ variants
def v_slatdot(ink, accent, paper, size=SIZE, track=TRACK):
    """J - the dot on the i becomes a slat.

    One glyph changes and nothing else moves. It is the smallest thing that can
    carry the product, and the only one of the five that still works at the
    size of a browser tab.
    """
    paths, marks, w = _pieces(size, track, dotless=True)
    pad = size * 0.5
    W, H = w + pad * 2, size * 1.9
    base_y = H * 0.66
    ix = [x for k, x in marks if k == "i"][0]
    bw = I_STEMW * size
    top = base_y - 0.760 * size
    bot = base_y - (XH + 0.075) * size
    body = (_paper(W, H, paper)
            + f'<g transform="translate({pad:.2f} 0)">'
            + _draw(paths, base_y, ink)
            + f'<rect x="{ix + I_STEMX * size - bw / 2:.2f}" y="{top:.2f}" '
              f'width="{bw:.2f}" height="{bot - top:.2f}" rx="{bw / 2:.2f}" '
              f'fill="{accent}"/></g>')
    return _svg(W, H, body), W, H


def v_stacked(ink, accent, paper, size=SIZE, track=TRACK):
    """K - the slats centred ABOVE the word.

    This slot was a fluted o. It is not, because at Jost Light's weight there
    is no good way in: slats cut through the ring break the letter into four
    arcs, and slats inside the counter read as a face. Two attempts, both
    measured, both binned - so the slot went to the lockup that was actually
    missing, the square one for an avatar or a stamp.
    """
    paths, marks, w = _pieces(size, track)
    n = 5
    slat_w = size * 0.055
    gap = slat_w * 0.85
    mark_w = n * slat_w + (n - 1) * gap
    pad = size * 0.5
    W = w + pad * 2
    H = size * 2.5
    base_y = H * 0.74
    top = base_y - size * 1.42
    bars = []
    for i in range(n):
        bx = (W - mark_w) / 2 + i * (slat_w + gap)
        shrink = size * 0.10 if i in (0, n - 1) else (size * 0.05 if i in (1, n - 2) else 0.0)
        bars.append(f'<rect x="{bx:.2f}" y="{top + shrink:.2f}" width="{slat_w:.2f}" '
                    f'height="{size * 0.50 - shrink * 2:.2f}" rx="{slat_w / 2:.2f}" '
                    f'fill="{accent if i == 2 else ink}"/>')
    body = (_paper(W, H, paper) + "".join(bars)
            + f'<g transform="translate({pad:.2f} 0)">' + _draw(paths, base_y, ink) + "</g>")
    return _svg(W, H, body), W, H


def v_underline(ink, accent, paper, size=SIZE, track=TRACK):
    """L - a run of slats under the word, the way a panel meets a floor."""
    paths, marks, w = _pieces(size, track)
    pad = size * 0.5
    W, H = w + pad * 2, size * 2.05
    base_y = H * 0.60
    # These are SLATS: taller than they are wide. The first version derived the
    # width from the wordmark's length, which at eleven bars made each one wider
    # than its own height - a row of horizontal lozenges, the opposite shape to
    # the product. Width is fixed now and the COUNT follows from it.
    # Fix the COUNT and derive the pitch, not the other way round. Filling the
    # width with a fixed slat size gave forty-four of them - a ruler, not a
    # panel.
    n = 9
    bar_h = size * 0.20
    top = base_y + size * 0.225
    pitch = w / n
    unit = size * 0.028          # ~1:7 - anything squarer renders as an oval
    bars = []
    for i in range(n):
        bx = pad + i * pitch + (pitch - unit) / 2
        bars.append(f'<rect x="{bx:.2f}" y="{top:.2f}" width="{unit:.2f}" '
                    f'height="{bar_h:.2f}" rx="{unit / 2:.2f}" '
                    f'fill="{accent if i == n // 2 else ink}"/>')
    body = (_paper(W, H, paper)
            + f'<g transform="translate({pad:.2f} 0)">' + _draw(paths, base_y, ink) + "</g>"
            + "".join(bars))
    return _svg(W, H, body), W, H


def v_slatmark(ink, accent, paper, size=SIZE, track=TRACK):
    """M - four bare slats to the left of the word.

    No badge, no rounded square, no box - round one already tried that and he
    passed on it. Just the slats, at the word's own height, so they read as a
    piece of panel rather than an icon someone dropped in.
    """
    paths, marks, w = _pieces(size, track)
    n = 4
    slat_w = size * 0.072
    gap = slat_w * 0.72
    mark_w = n * slat_w + (n - 1) * gap
    pad = size * 0.5
    lead = size * 0.42
    W, H = mark_w + lead + w + pad * 2, size * 1.9
    base_y = H * 0.66
    hi, lo = base_y - size * 0.76, base_y + size * 0.02
    bars = []
    for i in range(n):
        bx = pad + i * (slat_w + gap)
        # the outer two are short, the inner two full: a panel seen at an angle,
        # and it keeps the group from reading as a bar chart
        shrink = size * 0.13 if i in (0, n - 1) else 0.0
        bars.append(f'<rect x="{bx:.2f}" y="{hi + shrink:.2f}" width="{slat_w:.2f}" '
                    f'height="{lo - hi - shrink * 2:.2f}" rx="{slat_w / 2:.2f}" '
                    f'fill="{accent if i == 2 else ink}"/>')
    body = (_paper(W, H, paper) + "".join(bars)
            + f'<g transform="translate({pad + mark_w + lead:.2f} 0)">'
            + _draw(paths, base_y, ink) + "</g>")
    return _svg(W, H, body), W, H


def v_both(ink, accent, paper, size=SIZE, track=TRACK):
    """N - the slat dot and the slat underline together. The fullest version;
    whether it is one cue too many is the kind of thing he should look at
    rather than be told."""
    paths, marks, w = _pieces(size, track, dotless=True)
    pad = size * 0.5
    W, H = w + pad * 2, size * 2.05
    base_y = H * 0.60
    ix = [x for k, x in marks if k == "i"][0]
    bw = I_STEMW * size
    top = base_y - 0.760 * size
    bot = base_y - (XH + 0.075) * size
    n = 9
    bar_h = size * 0.20
    utop = base_y + size * 0.225
    pitch = w / n
    unit = size * 0.028
    bars = []
    for i in range(n):
        bx = pad + i * pitch + (pitch - unit) / 2
        bars.append(f'<rect x="{bx:.2f}" y="{utop:.2f}" width="{unit:.2f}" '
                    f'height="{bar_h:.2f}" rx="{unit / 2:.2f}" '
                    f'fill="{accent if i == n // 2 else ink}"/>')
    body = (_paper(W, H, paper)
            + f'<g transform="translate({pad:.2f} 0)">'
            + _draw(paths, base_y, ink)
            + f'<rect x="{ix + I_STEMX * size - bw / 2:.2f}" y="{top:.2f}" '
              f'width="{bw:.2f}" height="{bot - top:.2f}" rx="{bw / 2:.2f}" '
              f'fill="{accent}"/></g>'
            + "".join(bars))
    return _svg(W, H, body), W, H


VARIANTS = {"slatdot": v_slatdot, "stacked": v_stacked, "underline": v_underline,
            "slatmark": v_slatmark, "both": v_both}
LABEL = {"slatdot": "J - slat dot", "stacked": "K - slats above",
         "underline": "L - slat underline", "slatmark": "M - slat mark",
         "both": "N - slat dot + underline"}


def icon(kind, ink, accent, paper, size=512.0):
    """Square icon: the lowercase b, with the same slat cue where it fits."""
    d, w = text_path("b", "jost", size * 0.60, 0, size * 0.70)
    body = (f'<rect width="{size:.0f}" height="{size:.0f}" rx="{size * 0.19:.0f}" '
            f'fill="{ink}"/>'
            f'<g fill="{paper}" transform="translate({(size - w) / 2:.2f} 0)">{d}</g>')
    bw = size * 0.052
    body += (f'<rect x="{size / 2 - bw / 2 + size * 0.155:.2f}" y="{size * 0.185:.2f}" '
             f'width="{bw:.2f}" height="{size * 0.20:.2f}" rx="{bw / 2:.2f}" '
             f'fill="{accent}"/>')
    return _svg(size, size, body)


def main() -> None:
    import cairosvg
    want = sys.argv[1:] or list(VARIANTS)
    OUT.mkdir(parents=True, exist_ok=True)
    for k in want:
        if k not in VARIANTS:
            raise SystemExit(f"unknown variant {k}; have {list(VARIANTS)}")
        fn = VARIANTS[k]
        jobs = [("clay", CLAY, CLAY, PAPER),
                ("neutral", INKBLACK, INKBLACK, "#ffffff"),
                ("two-tone", INKBLACK, CLAY, "#ffffff"),
                ("reversed", PAPER, CLAY, "#2a2118")]
        for tag, ink, accent, paper in jobs:
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
        isvg = icon(k, CLAY, PAPER, PAPER)
        ib = OUT / f"{k}-icon"
        ib.with_suffix(".svg").write_text(isvg, encoding="utf-8")
        cairosvg.svg2png(bytestring=isvg.encode(), write_to=str(ib) + ".png",
                         output_width=512, output_height=512)
        print(f"{k:<10} {LABEL[k]}")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
