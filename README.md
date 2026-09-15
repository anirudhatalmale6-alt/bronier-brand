# Bronier — logo concepts

## BLACK is the answer (15 Sep)

*"also make the logo black. and all the colors black instead of brown. it's
better estetics."* So the delivered wordmark is **`out4/*-black.*`** — the
lowercase wordmark with the slats on the o, in `#141414`. The clay versions
stay in the repo only as history; do not send them.

The site matches: `bronier-web` is black and white throughout. The only colour
left anywhere is in the panel SWATCHES, because a customer choosing between oak
and anthracite needs to see oak and anthracite.

---

## Round 3 (`out3/`, `favicon3/`, `headers3/`) — current

*"Lowercase is good. Can you also try to create something related to my niche."*
So: the round-2 lowercase wordmark he picked, in his clay, with the panel slats
worked in five ways.

| | variant | note |
|---|---|---|
| J | `slatdot` | the dot on the i becomes a slat — quietest, first to vanish small |
| K | `stacked` | slats above the word — the SQUARE lockup, not a header logo |
| L | `underline` | a run of slats beneath |
| M | `slatmark` | slats beside the word — **recommended**, the only one still showing slats in the real header |
| N | `both` | slat dot + underline |

### Two things that did not survive

**A fluted lowercase o.** Slats cut through the ring broke the letter into four
arcs; slats inside the counter read as a face. Both measured, both binned — K is
that slot, reused for the lockup that was actually missing.

**`<mask>` does not work in cairosvg.** A positive control — black square, white
stripe masked out — came back solid black, while the same test with `clip-path`
was correct. Round 2's fluted O therefore rendered with **no grooves at all** in
every PNG, so the PNG and the SVG of the same logo disagreed. Both rounds now
use `_keep_bands()`, a clipPath of everything except the groove columns.

---

## Round 2 (`out2/`, `favicon2/`, `headers2/`) — current

His note: *"Something else, doesn't need to be brown color. Only Bronier.
Without decor."* So: the word BRONIER alone, no symbol, no DECOR, no brown,
nothing carried over from round one.

| | direction | colour |
|---|---|---|
| E | `fluted` | charcoal + amber — the O carries one vertical groove |
| F | `hairline` | black on white — **fragile below ~30px, faint on the brown header** |
| G | `serif` | deep green |
| H | `framed` | slate blue — **recommended**, with G |
| I | `lower` | clay, lowercase |

Each is built in three ways: `-colour` (its own palette), `-neutral` (plain
black, so the shape can be judged without the colour arguing) and `-reversed`
(light, for a dark header). Every one also exists as `-transparent`.

**His site is brown.** A black or charcoal wordmark drops onto it unchanged;
green, slate or clay means the site palette moves too. That is his decision,
not one to make quietly inside a logo file.

`python3 logo2.py` rebuilds; `python3 sheet2.py` makes the PDF.

---

## Round 1 (`out/`, `favicon/`, `headers/`) — superseded

Four directions for **bronier.mk** (decorative wall panels, Strumica, MK).
Nothing here is final: pick a letter and it gets refined.

| | concept | notes |
|---|---|---|
| A | `slat` | the B with the fluting cut into it |
| B | `panel` | fluted tile — **recommended**, holds down to 24px |
| C | `arch` | slats in an arch, the accent-wall shape |
| D | `word` | wordmark only — the closest to the current logo, fixed |

## What's in `out/`

For every concept and every colourway (`dark` for cream pages, `light` for the
brown header, `mono` for one-colour printing):

* `*-horizontal-*` — mark beside the wordmark
* `*-stacked-*` — mark above the wordmark
* `*-compact-*-transparent` — mark + BRONIER, no DECOR. **This is the header file.**
  At 44px tall DECOR renders about 4px high: present, unreadable, and just noise.
* `*-mark-*` — the square mark alone, 512px
* `*-transparent` — no background rectangle. **These are the real assets.**
  The versions with a painted background are for the presentation sheet only;
  dropped into the site header they sit in a visible block of almost-but-not-
  quite the header brown, which is one of the faults being fixed here.

`favicon/` carries `*-favicon.ico` (16/32/48 in one file) plus 16, 32, 48, 180
and 512px PNGs for each concept.

Every file exists as both `.svg` and `.png`. Use the SVG wherever you can — it
scales to a billboard with no blurring.

## Type

Lato, under the **SIL Open Font License 1.1** — free for commercial use. Every
letter is stored as an outline, not as live text, so the files render correctly
on a machine that has never had Lato installed.

## Colours

Taken from the site's own stylesheet rather than invented:

```
brown-900 #3a271a    brown-700 #5c3d24    brown-500 #7c5230
gold      #e0a94a    gold-dark #c1852c    cream     #f7f2ea
```

## Rebuilding

```
python3 logo.py            # all concepts, SVG + PNG
python3 logo.py panel      # just one
python3 header_mock.py     # drop each into the real site header and screenshot
python3 sheet.py           # the presentation PDF
```

`header_mock.py` is the check that matters: a logo approved on a white sheet and
then dropped into a brown gradient header next to a search box is how you find
out the lockup is too wide or the cream is the wrong cream.
