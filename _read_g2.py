"""Read the NEW CURVE guideline PDF: page count, colour values, typography rules."""
import re, sys
from pathlib import Path

import fitz  # pymupdf

PDF = Path(r"C:/Users/Orange/workspace/curve-site/CURVE BRAND GUIDELINE (1).pdf")
OUT = Path(r"C:/Users/Orange/workspace/curve-site/_g2")
OUT.mkdir(exist_ok=True)

doc = fitz.open(PDF)
print(f"الملف: {PDF.name} · {PDF.stat().st_size/1e6:.1f} MB · الصفحات: {len(doc)}")
print(f"مقاس أول صفحة: {doc[0].rect.width:.0f} × {doc[0].rect.height:.0f}\n")

KEY = re.compile(r"(727272|114|color|colour|background|typograph|poppins|RB|gray|grey|about\s*us|hex|cmyk|lab|header|body|caption|weight|size)", re.I)
full = []
for i, page in enumerate(doc):
    t = page.get_text().strip()
    full.append(t)
    hits = sorted({m.group(0).lower() for m in KEY.finditer(t)})
    if t:
        first = " | ".join(t.splitlines()[:3])[:110]
        print(f"ص{i+1:02d} ({len(t):5d} حرف) {hits[:8]}")
        if t:
            print(f"      {first}")
    else:
        print(f"ص{i+1:02d} (بلا نص — صورة)")

(OUT / "text.txt").write_text("\n\n".join(f"=== PAGE {i+1} ===\n{t}" for i, t in enumerate(full)), encoding="utf-8")
print(f"\nنص كامل → {OUT/'text.txt'} ({sum(len(t) for t in full)} حرف)")
