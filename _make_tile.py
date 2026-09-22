"""Build a seamless pattern tile out of Alaa's OFFICIAL geometric elements.

The guideline's pattern sampler (PATTERN & ELEMENTS-04) is a page export with big gaps
between its rows, so it does not tile. Instead the official elements themselves are
composed into one 120x120 tile with offset rows — the same rhythm the identity uses.
"""
import re
from pathlib import Path

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "assets" / "svg"

SRC = {
    "pinwheel": "element-pinwheel.svg",
    "corner":   "element-corner.svg",
    "arch":     "element-arch.svg",
    "rotor":    "element-rotor.svg",
    "hook":     "element-hook.svg",
}
TILE = 120.0
# (element, centre x, centre y, target width in tile units)
PLACEMENT = [
    ("pinwheel", 28, 28, 40),
    ("corner",   88, 22, 30),
    ("hook",     92, 82, 28),
    ("rotor",    26, 88, 28),
]

parts, missing = [], []
for name, x, y, w in PLACEMENT:
    p = OUT / SRC[name]
    if not p.exists():
        missing.append(name)
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    vb = re.search(r'viewBox="([-\d.\s]+)"', t)
    vx, vy, vw, vh = [float(v) for v in vb.group(1).split()]
    s = w / vw
    paths = re.findall(r"<path[^>]*/>|<path[^>]*>.*?</path>", t, re.S)
    body = "".join(paths)
    body = re.sub(r'fill="(?!none)[^"]*"', "", body)      # keep the default black ink
    body = re.sub(r'class="[^"]*"', "", body)
    parts.append(f'<g transform="translate({x - w/2:.2f},{y - (w*vh/vw)/2:.2f}) scale({s:.4f}) '
                 f'translate({-vx:.2f},{-vy:.2f})">{body}</g>')

svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
       f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TILE:.0f} {TILE:.0f}" '
       f'width="{TILE:.0f}" height="{TILE:.0f}" fill="#000000">\n  '
       + "\n  ".join(parts) + "\n</svg>\n")
(OUT / "pattern-tile.svg").write_text(svg, encoding="utf-8")
print(f"✓ assets/svg/pattern-tile.svg  ({len(svg)} حرف · {len(parts)} عنصر · مفقود: {missing or 'لا شي'})")

# معاينة PNG للتأكد
(OUT / ".." / ".." / "_tile_preview.html").write_text(
    '<!doctype html><meta charset="utf-8"><style>body{margin:0;background:#E5E5E5}'
    'div.band{height:84px;background-image:url("assets/svg/pattern-tile.svg");'
    'background-size:110px auto;background-repeat:repeat;background-position:center}'
    'div.big{height:300px;background-image:url("assets/svg/pattern-tile.svg");'
    'background-size:240px auto;background-repeat:repeat;margin-top:20px}</style>'
    '<div class="band"></div><div class="big"></div>', encoding="utf-8")
print("✓ _tile_preview.html")
