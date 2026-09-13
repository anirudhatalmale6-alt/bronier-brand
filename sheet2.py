#!/usr/bin/env python3
"""Round-2 presentation PDF. Refuses to write if a source image is missing."""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
OUT, HDR, FAV = ROOT / "out2", ROOT / "headers2", ROOT / "favicon2"
W, H = 1654, 1169
INK, PAPER = (28, 28, 28), (255, 255, 255)
ORDER = ["fluted", "hairline", "serif", "framed", "lower"]
LABEL = {"fluted": "E  -  ACCENT O", "hairline": "F  -  HAIRLINE",
         "serif": "G  -  SERIF", "framed": "H  -  FRAMED",
         "lower": "I  -  LOWERCASE"}
COLOUR = {"fluted": "charcoal + amber", "hairline": "black on white",
          "serif": "deep green", "framed": "slate blue", "lower": "clay"}

def F(s, b=False):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""), s)

def page(title, sub=""):
    p = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(p)
    d.rectangle((0, 0, W, 92), fill=INK)
    d.text((60, 28), title, font=F(36, True), fill=(255, 255, 255))
    if sub: d.text((60, 112), sub, font=F(23), fill=(110, 110, 110))
    return p, d

def fit(im, bw, bh):
    r = min(bw / im.width, bh / im.height)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)

pages, missing = [], []

c = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(c)
d.rectangle((0, 0, W, 175), fill=INK)
d.text((64, 52), "BRONIER  -  round two", font=F(50, True), fill=(255, 255, 255))
d.text((64, 122), "12 September 2026", font=F(24), fill=(180, 180, 180))
y = 235
for t, b in [("Your note: something else, no brown, only Bronier, without DECOR.", True), ("", False),
  ("So all five below are the word BRONIER on its own. No symbol, no DECOR, no brown,", False),
  ("and nothing carried over from the first set.", False), ("", False),
  ("One thing that is your call, not mine", True),
  ("Your site is brown. A black or charcoal logo drops onto it with nothing else changing.", False),
  ("Green, slate or clay means the site's colours move with the logo - that is a bigger job", False),
  ("than the logo, so I want you to choose it rather than find out later.", False),
  ("Because of that, every direction is also drawn in plain black in the download, so you", False),
  ("can judge the shape without the colour arguing with it.", False), ("", False),
  ("Page 4 is the one to look at", True),
  ("It is your real site header with each logo dropped in. Two of them do not hold up there,", False),
  ("and I would rather tell you that now than after you picked one.", False), ("", False),
  ("Fonts are Lato, Jost and Latin Modern - all free for commercial use. Letters are saved", False),
  ("as outlines, so the files print correctly on any computer.", False)]:
    d.text((64, y), t, font=F(27, b), fill=INK if b else (80, 80, 80)); y += 39
pages.append(c)

for tag, title in (("colour", "Five directions  -  in colour"),
                   ("neutral", "The same five  -  in plain black")):
    p, d = page(title, "" if tag == "colour" else
                "so the shape can be judged with the colour question set aside")
    yy = 140
    for k in ORDER:
        f = OUT / f"{k}-{tag}.png"
        if not f.exists(): missing.append(f.name); continue
        im = fit(Image.open(f).convert("RGB"), 1090, 168)
        d.text((60, yy + im.height // 2 - 20), LABEL[k], font=F(21, True), fill=INK)
        if tag == "colour":
            d.text((60, yy + im.height // 2 + 4), COLOUR[k], font=F(18), fill=(130, 130, 130))
        p.paste(im, (420, yy))
        yy += im.height + 20
    pages.append(p)

p, d = page("In your real site header", "the live page with each logo swapped in")
yy = 132
for n in ["current"] + ORDER:
    f = HDR / f"header-{n}.png"
    if not f.exists(): missing.append(f.name); continue
    im = fit(Image.open(f).convert("RGB"), 1500, 132)
    d.text((60, yy), "CURRENT" if n == "current" else LABEL[n], font=F(18, True), fill=INK)
    p.paste(im, (60, yy + 22)); yy += im.height + 48
pages.append(p)

p, d = page("Browser tab icon", "512 / 64 / 44 / 32 / 24 px  -  the icon is the word's own first letter")
yy = 175
for k in ORDER:
    d.text((60, yy + 44), LABEL[k], font=F(21, True), fill=INK)
    x = 420
    src = OUT / f"{k}-icon.png"
    if not src.exists(): missing.append(src.name); continue
    base = Image.open(src).convert("RGB")
    for s in (128, 64, 44, 32, 24):
        p.paste(base.resize((s, s), Image.LANCZOS), (x, yy + (128 - s) // 2)); x += 150
    yy += 155
pages.append(p)

p, d = page("What I would pick, and what is weak")
y = 140
for t, b in [("H - FRAMED, or G - SERIF.", True),
  ("Both hold up in the header, both look like a company that sells finished interiors", False),
  ("rather than building material, and both work in one colour on an invoice.", False), ("", False),
  ("E - ACCENT O is the one with a bit of the product in it: the O carries a single", True),
  ("vertical line, the way the panels are grooved. The quietest way to say what you sell.", False), ("", False),
  ("Where I would be careful", True),
  ("F - HAIRLINE is beautiful big and disappears small. On your brown header it is already", False),
  ("faint - look at page 4 - and below about 30px the strokes start to break up. It works", False),
  ("if the header goes white or black. On brown it does not.", False), ("", False),
  ("I - LOWERCASE has the same problem, less severely. It is the most modern of the five", False),
  ("and it wants a pale background to sit on.", False), ("", False),
  ("Tell me a letter", True),
  ("Then I tune it properly - spacing, weight, the exact colour - build the full file set,", False),
  ("and put it on the site. A Cyrillic version is no extra work if you want one.", False)]:
    d.text((64, y), t, font=F(27, b), fill=INK if b else (80, 80, 80)); y += 39
pages.append(p)

if missing:
    sys.exit("REFUSING to write - missing: %s" % sorted(set(missing)))
out = "/var/lib/freelancer/projects/40523265/bronier-logo-round2.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=140)
print("wrote", out, len(pages), "pages")
