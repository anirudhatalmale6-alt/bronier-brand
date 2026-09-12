#!/usr/bin/env python3
"""Put each candidate into the REAL site header and photograph the result.

A logo approved on a white sheet and then dropped into a brown gradient header
next to a search box is how you find out the lockup is too wide or the cream is
the wrong cream. So the mark is swapped into the live staging page as a data:
URI and the header strip is captured from the browser - same CSS, same
neighbours, same 44px height rule the theme enforces.
"""
import base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
SHOTS = ROOT / "headers"; SHOTS.mkdir(exist_ok=True)
URL = "https://bronier.185.103.164.237.nip.io/"
# The header sits on brown, so each candidate's LIGHT lockup is the one that
# belongs there - that is the whole point of having made one.
CANDS = [("current", None),
         ("slat", "slat-compact-light-transparent.png"),
         ("panel", "panel-compact-light-transparent.png"),
         ("arch", "arch-compact-light-transparent.png"),
         ("word", "word-horizontal-light-transparent.png")]

with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1280, "height": 400})
    for name, f in CANDS:
        pg.goto(URL, wait_until="networkidle", timeout=60000)
        if f:
            b64 = base64.b64encode((OUT / f).read_bytes()).decode()
            pg.eval_on_selector(".logo-img", "(e,d)=>{e.src=d;e.srcset='';}",
                                f"data:image/png;base64,{b64}")
            pg.wait_for_timeout(900)
        el = pg.query_selector(".site-header") or pg.query_selector("header")
        el.screenshot(path=str(SHOTS / f"header-{name}.png"))
        box = el.bounding_box()
        print(f"{name:<8} header {box['width']:.0f}x{box['height']:.0f}")
    br.close()
