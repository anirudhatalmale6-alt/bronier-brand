#!/usr/bin/env python3
"""The presentation PDF. Screenshots do not open in his Freelancer chat, so a
PDF is the only way he sees any of this - and it refuses to write a short file
rather than quietly dropping a page."""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
OUT, HDR, FAV = ROOT / "out", ROOT / "headers", ROOT / "favicon"
W, H = 1654, 1169
CREAM, BROWN, INK, GOLD = (247,242,234), (124,82,48), (58,39,26), (224,169,74)
LABEL = {"slat":"A  -  SLAT B","panel":"B  -  PANEL","arch":"C  -  ARCH","word":"D  -  WORDMARK"}
ORDER = ["slat","panel","arch","word"]

def F(s,b=False):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf"%("-Bold" if b else ""), s)

def page(title, sub=""):
    p = Image.new("RGB",(W,H),(255,255,255)); d = ImageDraw.Draw(p)
    d.rectangle((0,0,W,96), fill=BROWN)
    d.text((64,30), title, font=F(38,True), fill=(255,255,255))
    if sub: d.text((64,120), sub, font=F(24), fill=(110,95,80))
    return p, d

def fit(im, bw, bh):
    r = min(bw/im.width, bh/im.height)
    return im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)

pages, missing = [], []

# ---- cover
c = Image.new("RGB",(W,H),CREAM); d = ImageDraw.Draw(c)
d.rectangle((0,0,W,190), fill=BROWN)
d.text((70,62), "BRONIER  -  logo concepts", font=F(52,True), fill=(255,255,255))
d.text((70,132), "12 September 2026", font=F(26), fill=(230,214,194))
y = 250
for t,b in [("Four directions. Nothing is final - pick one and I refine it.", True),("",False),
  ("What is wrong with the logo you have now", True),
  ("It sets DECOR through the middle of the letters N and I. At the size the site actually", False),
  ("uses it - 44 pixels tall - that word closes up into a smudge. It is also black only, so", False),
  ("on your brown header it is nearly invisible (see the header page).", False),("",False),
  ("What each of these has to do", True),
  ("-  stay readable at 44px in the header and 32px as a browser-tab icon", False),
  ("-  have a light version that sits straight on the brown header, with no white box", False),
  ("-  use the brown, gold and cream already in your site, not a new palette", False),
  ("-  carry something of the product: these are vertical fluted panels, which is a shape,", False),
  ("   not a metaphor I had to invent", False),("",False),
  ("Type is Lato, under the SIL Open Font License - free for commercial use. The letters are", False),
  ("saved as outlines, so the files print correctly on a computer that does not have the font.", False)]:
    d.text((70,y), t, font=F(29,b), fill=INK if b else (85,72,60)); y += 41
pages.append(c)

# ---- concepts on cream, then on brown
for scheme, title, bg in (("dark","The four concepts  -  on cream", (255,255,255)),
                          ("light","The four concepts  -  on brown", (255,255,255))):
    p, d = page(title)
    yy = 130
    for c_ in ORDER:
        f = OUT/f"{c_}-horizontal-{scheme}.png"
        if not f.exists(): missing.append(f.name); continue
        im = fit(Image.open(f).convert("RGB"), 1180, 215)
        d.text((64, yy+im.height//2-14), LABEL[c_], font=F(23,True), fill=INK)
        p.paste(im, (380, yy))
        yy += im.height + 26
    pages.append(p)

# ---- small sizes
p, d = page("Does it survive when it is small?",
            "128 / 64 / 44 / 32 / 24 px  -  44px is the site header, 32px is the browser tab")
yy = 190
for c_ in ORDER:
    d.text((64, yy+40), LABEL[c_], font=F(23,True), fill=INK)
    x = 380
    for s in (128,64,44,32,24):
        f = FAV/f"{c_}-{'512' if s>180 else ('180' if s>48 else ('48' if s>32 else ('32' if s>16 else '16')))}.png"
        src = OUT/f"{c_}-mark-dark.png"
        im = Image.open(src).convert("RGB").resize((s,s), Image.LANCZOS)
        p.paste(im, (x, yy+ (128-s)//2)); x += 150
    yy += 160
pages.append(p)

# ---- real header
p, d = page("In your actual site header", "the real page, the logo swapped in - not a mock-up")
yy = 150
for name in ["current"]+ORDER:
    f = HDR/f"header-{name}.png"
    if not f.exists(): missing.append(f.name); continue
    im = fit(Image.open(f).convert("RGB"), 1520, 150)
    d.text((64, yy), "CURRENT" if name=="current" else LABEL[name], font=F(20,True), fill=INK)
    p.paste(im, (64, yy+26)); yy += im.height + 58
pages.append(p)

# ---- recommendation
p, d = page("What I would pick, and what happens next")
y = 150
for t,b in [("My recommendation: B - PANEL, with C - ARCH a close second.", True),
  ("Both stay clean all the way down to 24px, both look like the product without", False),
  ("spelling it out, and both sit on the brown header without a box.", False),("",False),
  ("Being straight about A - SLAT B: it is the weakest of the four small. The grooves", False),
  ("start closing up below about 32px. If you like that direction I would use the plain", False),
  ("B from D as the browser-tab icon and keep the fluted one for large use.", False),("",False),
  ("D - WORDMARK is the closest to what you have now, fixed: proper letter spacing,", False),
  ("DECOR on its own line under a gold rule instead of buried inside the letters.", False),("",False),
  ("Every concept already comes with:", True),
  ("-  horizontal, stacked and compact lockups", False),
  ("-  a dark version for cream pages and a light one for the brown header", False),
  ("-  transparent PNG and SVG (SVG scales to any size with no blurring)", False),
  ("-  favicon.ico plus 16/32/48/180/512 px icons", False),("",False),
  ("Tell me a letter and I will refine it - spacing, weight, the gold, a Cyrillic", True),
  ("version of the wordmark if you want one - and then put it live on the site.", True)]:
    d.text((70,y), t, font=F(28,b), fill=INK if b else (85,72,60)); y += 40
pages.append(p)

if missing:
    sys.exit("REFUSING to write - missing source images: %s" % sorted(set(missing)))
out = "/var/lib/freelancer/projects/40523265/bronier-logo-concepts.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=140)
print("wrote", out, len(pages), "pages")
