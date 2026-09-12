#!/usr/bin/env python3
"""Logo concepts for bronier.mk - decorative wall panels, Strumica MK.

    python3 logo.py            # every concept, every lockup, SVG + PNG
    python3 logo.py slat       # one concept

Why a new mark was needed at all. The existing one sets BRONIER in a tight
high-contrast didone with DECOR knocked out THROUGH the middle of the N and I.
At the size it is actually used - 44px tall in the site header, and 32px as a
favicon - the counters close up and DECOR turns into a smudge inside a letter.
It is also black only, so on the brown header it has to sit in a white box.

So the brief each concept is held to:
  * legible at 44px tall and recognisable at 32px square;
  * a light version that sits DIRECTLY on the brown header, no box;
  * built from the brand palette already in style.css, not a new one;
  * something of the product in it - these are vertical fluted slat panels,
    which is a shape, not a metaphor I have to invent.

Type is Lato (SIL Open Font License 1.1) - free to use commercially, and he
owns the outlines once they are drawn as paths here. Nothing in the output
depends on a font being installed on his machine.
"""
from __future__ import annotations

import pathlib
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
FONTS = {
    "black": "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
    "heavy": "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf",
    "bold": "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "regular": "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
    "light": "/usr/share/fonts/truetype/lato/Lato-Light.ttf",
}

# Straight out of the theme's :root - a logo that invents its own brown is a
# logo that will never quite match the site it sits on.
BROWN_900 = "#3a271a"
BROWN_700 = "#5c3d24"
BROWN_500 = "#7c5230"
BROWN_400 = "#8f6337"
GOLD = "#e0a94a"
GOLD_DK = "#c1852c"
CREAM = "#f7f2ea"
WHITE = "#ffffff"

_cache: dict[str, TTFont] = {}


def _font(weight: str) -> TTFont:
    if weight not in _cache:
        _cache[weight] = TTFont(FONTS[weight])
    return _cache[weight]


def text_path(s: str, weight: str, size: float, x: float, y: float,
              tracking: float = 0.0) -> tuple[str, float]:
    """One SVG path for a whole string, plus the width it occupied.

    Every glyph is converted to outlines. That is the difference between a logo
    and a screenshot of a font: outlines render identically on a machine that
    has never heard of Lato, which is every machine his printer uses.

    `tracking` is in em, added between glyphs. Letterspacing is doing real work
    in three of these concepts, so it is a parameter rather than a constant.
    """
    f = _font(weight)
    upem = f["head"].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    scale = size / upem
    parts = []
    pen_x = x
    for ch in s:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"no glyph for {ch!r} in {weight}")
        pen = SVGPathPen(gs)
        gs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            # y is flipped: font space is up-positive, SVG is down-positive.
            parts.append(f'<path d="{d}" transform="translate({pen_x:.2f} {y:.2f}) '
                         f'scale({scale:.5f} {-scale:.5f})"/>')
        pen_x += gs[gname].width * scale + tracking * size
    if s:
        pen_x -= tracking * size          # no tracking after the last letter
    return "".join(parts), pen_x - x


def text_width(s: str, weight: str, size: float, tracking: float = 0.0) -> float:
    return text_path(s, weight, size, 0, 0, tracking)[1]


# --------------------------------------------------------------- the marks
def slats(x, y, w, h, n, gap_ratio, colour, accent, accent_i, radius):
    """A row of vertical slats - the shape the product actually is.

    Widths are equal and the gaps are a ratio of the slat, so the rhythm holds
    at any size instead of the gaps vanishing first when the mark is scaled to
    a favicon.
    """
    unit = w / (n + (n - 1) * gap_ratio)
    gap = unit * gap_ratio
    out = []
    for i in range(n):
        sx = x + i * (unit + gap)
        c = accent if i == accent_i else colour
        out.append(f'<rect x="{sx:.2f}" y="{y:.2f}" width="{unit:.2f}" '
                   f'height="{h:.2f}" rx="{min(radius, unit / 2):.2f}" fill="{c}"/>')
    return "".join(out)


def mark_slat_b(size, fg, accent, bg_tile):
    """Concept SLAT B - the letter B cut into slats.

    The B is a real Lato Black outline used as a clipping path, so the slats
    are the letter rather than sitting next to it. That is the whole idea: the
    monogram is made of the product.
    """
    d, w = text_path("B", "black", size * 0.86, 0, size * 0.845)
    dx = (size - w) / 2                       # centre the glyph in the tile
    # The first version clipped the B out of seven full-height slats. The result
    # was a letter chopped into disconnected blocks - at 32px it read as an E.
    # So the B stays SOLID and the fluting is cut INTO it as three narrow
    # grooves, which is also how the panels are actually made.
    # The grooves must clear the STEM. At x = 0.16w the first one landed on the
    # left upright and shaved a loose sliver off it, so the mark read as "IB".
    # Lato Black's B carries its stem across roughly the first quarter of the
    # glyph, so the fluting starts at 0.34w and only the bowls are fluted.
    groove = size * 0.05
    x0 = dx + w * 0.34
    step = w * 0.20
    grooves = "".join(
        f'<rect x="{x0 + i * step:.2f}" y="-1" width="{groove:.2f}" '
        f'height="{size + 2:.2f}" fill="{bg_tile}"/>' for i in range(2))
    gold_bar = (f'<rect x="{x0 + 2 * step:.2f}" y="-1" width="{groove * 1.4:.2f}" '
                f'height="{size + 2:.2f}" fill="{accent}"/>')
    body = (f'<rect width="{size}" height="{size}" rx="{size * 0.2:.2f}" fill="{bg_tile}"/>'
            f'<g clip-path="url(#clipB)">'
            f'<rect width="{size}" height="{size}" fill="{fg}"/>{grooves}{gold_bar}'
            f"</g>")
    defs = (f'<clipPath id="clipB"><g transform="translate({dx:.2f} 0)">{d}</g></clipPath>')
    return body, defs


def mark_panel(size, fg, accent, bg_tile):
    """Concept PANEL - a fluted tile. The plainest of the four and the one that
    survives smallest; at 32px it is still a recognisable rhythm."""
    body = (f'<rect width="{size}" height="{size}" rx="{size * 0.2:.2f}" fill="{bg_tile}"/>'
            + slats(size * 0.17, size * 0.17, size * 0.66, size * 0.66, 5, 0.36,
                    fg, accent, 3, size * 0.04))
    return body, ""


def mark_arch(size, fg, accent, bg_tile):
    """Concept ARCH - slats inside an arch. This is what his own product photos
    look like on an accent wall, and the arch is the shape interior brands are
    using now. Costs the most detail at favicon size of the three marks."""
    r = size * 0.42
    cx = size / 2
    top = size * 0.12
    bottom = size * 0.9
    arch = (f'<path d="M {cx - r:.2f} {bottom:.2f} L {cx - r:.2f} {top + r:.2f} '
            f'A {r:.2f} {r:.2f} 0 0 1 {cx + r:.2f} {top + r:.2f} '
            f'L {cx + r:.2f} {bottom:.2f} Z"/>')
    body = (f'<rect width="{size}" height="{size}" rx="{size * 0.2:.2f}" fill="{bg_tile}"/>'
            f'<g clip-path="url(#clipA)">'
            + slats(cx - r, top - 1, r * 2, bottom - top + 2, 6, 0.30, fg, accent, 3,
                    size * 0.02)
            + "</g>")
    return body, f'<clipPath id="clipA">{arch}</clipPath>'


MARKS = {"slat": mark_slat_b, "panel": mark_panel, "arch": mark_arch}


# ------------------------------------------------------------ the lockups
def lockup(concept: str, ink: str, accent: str, tile: str, bg: str | None,
           word_ink: str, stacked: bool = False,
           compact: bool = False) -> tuple[str, int, int]:
    """`ink` colours the slats INSIDE the tile; `word_ink` colours the wordmark
    OUTSIDE it. They were one parameter and the first render put cream letters
    on a cream sheet - invisible, and the kind of thing a colour name hides.

    `bg=None` paints no background rectangle. That is what a real logo FILE is:
    dropped into the site header, every version with a painted background sat
    in a visible block of almost-but-not-quite the header brown - the same
    fault I am replacing the old logo for. Presentation sheets pass a colour;
    the delivered assets do not.

    `compact=True` drops DECOR. In the header the lockup is 44px tall, which
    puts DECOR at about 4px - present, unreadable, and just noise round the
    mark. Returns svg, width, height."""
    name_size = 108.0
    name_track = 0.14
    sub_size = 30.0
    sub_track = 0.52
    name_w = text_width("BRONIER", "black", name_size, name_track)
    sub_w = text_width("DECOR", "bold", sub_size, sub_track)

    if concept == "word":
        # No mark. The wordmark concept has to carry the whole identity, so it
        # gets the rule-and-descender treatment the current logo is reaching
        # for and missing.
        pad = 60
        w = int(name_w + pad * 2)
        h = 300
        name_d, _ = text_path("BRONIER", "black", name_size, pad, 150, name_track)
        rule_y = 182
        sub_d, _ = text_path("DECOR", "bold", sub_size, pad + (name_w - sub_w) / 2,
                             233, sub_track)
        body = (_bg(w, h, bg)
                + f'<g fill="{word_ink}">{name_d}</g>'
                f'<rect x="{pad}" y="{rule_y}" width="{name_w:.2f}" height="3" fill="{accent}"/>'
                f'<g fill="{word_ink}">{sub_d}</g>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                f'viewBox="0 0 {w} {h}">{body}</svg>', w, h)

    msize = 200.0
    mark_body, defs = MARKS[concept](msize, ink, accent, tile)

    if stacked:
        w = int(max(msize, name_w) + 120)
        h = 470
        mx = (w - msize) / 2
        name_d, _ = text_path("BRONIER", "black", name_size, (w - name_w) / 2, 372,
                              name_track)
        sub_d, _ = text_path("DECOR", "bold", sub_size, (w - sub_w) / 2, 420, sub_track)
        body = (_bg(w, h, bg)
                + f'<g transform="translate({mx:.2f} 60)">{mark_body}</g>'
                + f'<g fill="{word_ink}">{name_d}{sub_d}</g>')
    else:
        pad = 56
        gap = 46
        w = int(pad + msize + gap + name_w + pad)
        h = 312
        name_y = 168
        name_d, _ = text_path("BRONIER", "black", name_size, pad + msize + gap,
                              name_y, name_track)
        sub_d = "" if compact else text_path(
            "DECOR", "bold", sub_size, pad + msize + gap, name_y + 48, sub_track)[0]
        if compact:
            h = 280
            name_y = 190
            name_d, _ = text_path("BRONIER", "black", name_size,
                                  pad + msize + gap, name_y, name_track)
        body = (_bg(w, h, bg)
                + f'<g transform="translate({pad} {(h - msize) / 2:.2f})">{mark_body}</g>'
                + f'<g fill="{word_ink}">{name_d}{sub_d}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>', w, h)


def _bg(w, h, bg):
    return "" if bg is None else f'<rect width="{w}" height="{h}" fill="{bg}"/>'


def mark_only(concept: str, ink: str, accent: str, tile: str) -> str:
    """The square mark on its own - app icon, favicon, social avatar."""
    size = 512.0
    if concept == "word":
        # The wordmark concept still needs a square. A B in the brand brown is
        # the honest reduction of it - inventing a symbol here would mean the
        # favicon belongs to a logo that does not exist.
        d, w = text_path("B", "black", size * 0.62, 0, size * 0.73)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size:.0f}" '
                f'height="{size:.0f}" viewBox="0 0 {size:.0f} {size:.0f}">'
                f'<rect width="{size:.0f}" height="{size:.0f}" rx="{size * 0.2:.0f}" fill="{tile}"/>'
                f'<g fill="{ink}" transform="translate({(size - w) / 2:.2f} 0)">{d}</g>'
                f'<rect x="{size * 0.3:.0f}" y="{size * 0.78:.0f}" width="{size * 0.4:.0f}" '
                f'height="{size * 0.045:.0f}" rx="{size * 0.02:.0f}" fill="{accent}"/></svg>')
    body, defs = MARKS[concept](size, ink, accent, tile)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size:.0f}" '
            f'height="{size:.0f}" viewBox="0 0 {size:.0f} {size:.0f}">'
            f'<defs>{defs}</defs>{body}</svg>')


# --------------------------------------------------------------------- main
#: ink, accent, tile, background. "dark" is for cream pages; "light" is the one
#: that sits straight on the brown header, which the current logo cannot do.
SCHEMES = {
    "dark":  dict(ink=CREAM, accent=GOLD,  tile=BROWN_500, bg=CREAM,     word_ink=BROWN_900),
    "light": dict(ink=BROWN_500, accent=GOLD_DK, tile=CREAM, bg=BROWN_500, word_ink=CREAM),
    "mono":  dict(ink=WHITE, accent=WHITE, tile=BROWN_900, bg=WHITE,     word_ink=BROWN_900),
}
# The wordmark concept has no tile, so its ink has to be the readable one.
WORD_SCHEMES = {
    "dark":  dict(ink=BROWN_900, accent=GOLD, tile=BROWN_500, bg=CREAM,     word_ink=BROWN_900),
    "light": dict(ink=CREAM, accent=GOLD,     tile=CREAM,     bg=BROWN_500, word_ink=CREAM),
    "mono":  dict(ink=BROWN_900, accent=BROWN_900, tile=BROWN_900, bg=WHITE, word_ink=BROWN_900),
}
CONCEPTS = ["slat", "panel", "arch", "word"]


def main() -> None:
    import cairosvg
    want = sys.argv[1:] or CONCEPTS
    OUT.mkdir(parents=True, exist_ok=True)
    for c in want:
        if c not in CONCEPTS:
            raise SystemExit(f"unknown concept {c}; have {CONCEPTS}")
        schemes = WORD_SCHEMES if c == "word" else SCHEMES
        for sname, sch in schemes.items():
            for stacked in ([False] if c == "word" else [False, True]):
                svg, w, h = lockup(c, sch["ink"], sch["accent"], sch["tile"],
                                   sch["bg"], sch["word_ink"], stacked)
                tag = "stacked" if stacked else "horizontal"
                base = OUT / f"{c}-{tag}-{sname}"
                base.with_suffix(".svg").write_text(svg, encoding="utf-8")
                cairosvg.svg2png(bytestring=svg.encode(), write_to=str(base) + ".png",
                                 output_width=w * 2, output_height=h * 2)
                # the same lockup with NO background - the file he actually uses
                tsvg, tw, th = lockup(c, sch["ink"], sch["accent"], sch["tile"],
                                      None, sch["word_ink"], stacked)
                tb = OUT / f"{c}-{tag}-{sname}-transparent"
                tb.with_suffix(".svg").write_text(tsvg, encoding="utf-8")
                cairosvg.svg2png(bytestring=tsvg.encode(), write_to=str(tb) + ".png",
                                 output_width=tw * 2, output_height=th * 2)
            if c != "word":
                csvg, cw, ch = lockup(c, sch["ink"], sch["accent"], sch["tile"],
                                      None, sch["word_ink"], False, compact=True)
                cb = OUT / f"{c}-compact-{sname}-transparent"
                cb.with_suffix(".svg").write_text(csvg, encoding="utf-8")
                cairosvg.svg2png(bytestring=csvg.encode(), write_to=str(cb) + ".png",
                                 output_width=cw * 2, output_height=ch * 2)
            m = mark_only(c, sch["ink"], sch["accent"], sch["tile"])
            mb = OUT / f"{c}-mark-{sname}"
            mb.with_suffix(".svg").write_text(m, encoding="utf-8")
            cairosvg.svg2png(bytestring=m.encode(), write_to=str(mb) + ".png",
                             output_width=512, output_height=512)
        print(f"{c}: written")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
