# Bronier — logo concepts

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
