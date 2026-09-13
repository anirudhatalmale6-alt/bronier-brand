#!/usr/bin/env python3
"""Round-3 PDF. Refuses to write short."""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = pathlib.Path(__file__).resolve().parent
OUT, HDR = ROOT / "out3", ROOT / "headers3"
W, H = 1654, 1169
INK = (28, 28, 28); CLAY = (168, 80, 58)
ORDER = ["slatdot", "stacked", "underline", "slatmark", "both"]
LABEL = {"slatdot": "J  -  slat dot", "stacked": "K  -  slats above",
         "underline": "L  -  slat underline", "slatmark": "M  -  slat mark",
         "both": "N  -  slat dot + underline"}
NOTE = {"slatdot": "the dot on the i becomes a panel slat",
        "stacked": "slats centred above the word - the square lockup",
        "underline": "a run of slats under the word",
        "slatmark": "slats beside the word",
        "both": "the slat dot and the underline together"}
def F(s, b=False):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if b else ""), s)
def page(t, sub=""):
    p = Image.new("RGB", (W, H), (255,255,255)); d = ImageDraw.Draw(p)
    d.rectangle((0,0,W,92), fill=INK); d.text((60,28), t, font=F(36,True), fill=(255,255,255))
    if sub: d.text((60,112), sub, font=F(23), fill=(110,110,110))
    return p, d
def fit(im, bw, bh):
    r = min(bw/im.width, bh/im.height)
    return im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
pages, missing = [], []

c = Image.new("RGB",(W,H),(255,255,255)); d = ImageDraw.Draw(c)
d.rectangle((0,0,W,175), fill=CLAY)
d.text((64,52), "bronier  -  round three", font=F(50,True), fill=(255,255,255))
d.text((64,122), "13 September 2026", font=F(24), fill=(250,235,228))
y = 235
for t,b in [("You liked the lowercase, and asked for something from your niche in it.", True), ("",False),
 ("So all five below are the SAME lowercase wordmark you picked, in the same clay.", False),
 ("The only thing that changes is how the panel slats come into it.", False),("",False),
 ("The slats are the product itself - your WPC panels are vertical fluting. It is a shape", False),
 ("you already sell, so nothing here is a symbol I invented and hoped meant something.", False),("",False),
 ("A correction on the last set", True),
 ("Concept E had a fluted O. The grooves never appeared in the files I sent you - the tool", False),
 ("that turns my drawings into pictures silently ignores the instruction I used to cut them.", False),
 ("What you saw was a plain O with one amber line. It is fixed, and I found it because I", False),
 ("tested it here rather than trusting it. Nothing else in that set was affected.", False),("",False),
 ("I also dropped a fluted lowercase o from this round", True),
 ("Slats through the ring broke the letter into four pieces; slats inside the hole read as", False),
 ("a face. Two honest attempts, both binned. K is that slot, used for the square lockup", False),
 ("instead - the one you need for a profile picture or a stamp.", False)]:
    d.text((64,y), t, font=F(27,b), fill=INK if b else (80,80,80)); y += 39
pages.append(c)

p, d = page("Five ways the niche comes in", "same wordmark, same clay - only the slats change")
yy = 140
for k in ORDER:
    f = OUT/f"{k}-clay.png"
    if not f.exists(): missing.append(f.name); continue
    im = fit(Image.open(f).convert("RGB"), 1020, 172)
    d.text((60, yy+im.height//2-22), LABEL[k], font=F(21,True), fill=INK)
    d.text((60, yy+im.height//2+4), NOTE[k], font=F(17), fill=(130,130,130))
    p.paste(im, (470, yy)); yy += im.height + 18
pages.append(p)

p, d = page("In your real site header", "the live page with each one swapped in")
yy = 128
for n in ["current"]+ORDER:
    f = HDR/f"header-{n}.png"
    if not f.exists(): missing.append(f.name); continue
    im = fit(Image.open(f).convert("RGB"), 1500, 118)
    d.text((60, yy), "CURRENT" if n=="current" else LABEL[n], font=F(18,True), fill=INK)
    p.paste(im, (60, yy+22)); yy += im.height + 44
pages.append(p)

p, d = page("Small", "512 / 64 / 44 / 32 / 24 px")
yy = 175
for k in ORDER:
    src = OUT/f"{k}-icon.png"
    if not src.exists(): missing.append(src.name); continue
    d.text((60, yy+44), LABEL[k], font=F(21,True), fill=INK)
    base = Image.open(src).convert("RGB"); x = 470
    for s in (128,64,44,32,24):
        p.paste(base.resize((s,s), Image.LANCZOS), (x, yy+(128-s)//2)); x += 150
    yy += 155
pages.append(p)

p, d = page("What I would pick")
y = 140
for t,b in [("M - slat mark, then N.", True),
 ("M is the one that still shows the slats in your header at real size - look at page 3.", False),
 ("The slats sit at the height of the word, so they read as a piece of panel rather than", False),
 ("an icon dropped next to the name.", False),("",False),
 ("J is the quietest and the cleverest - one glyph changes and nothing else moves. It is", True),
 ("also the one where the idea disappears first when the logo gets small.", False),("",False),
 ("K is not a header logo - the word goes small to make room above it. It is the square", False),
 ("one: profile picture, stamp, a sticker on a box.", False),("",False),
 ("All five are the same word in the same colour, so you are only choosing how loud the", False),
 ("panel reference is. Tell me a letter and I will finish it and put it on the site.", True)]:
    d.text((64,y), t, font=F(27,b), fill=INK if b else (80,80,80)); y += 39
pages.append(p)

if missing: sys.exit("REFUSING to write - missing: %s" % sorted(set(missing)))
out = "/var/lib/freelancer/projects/40523265/bronier-logo-round3.pdf"
pages[0].save(out, save_all=True, append_images=pages[1:], resolution=140)
print("wrote", out, len(pages), "pages")
