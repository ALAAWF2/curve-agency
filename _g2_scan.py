"""Render the new guideline and find WHERE the #727272 (114,114,114) tint is actually used."""
import numpy as np, pymupdf
from pathlib import Path
from PIL import Image
from collections import Counter

PDF = Path(r"C:/Users/Orange/workspace/curve-site/CURVE BRAND GUIDELINE (1).pdf")
OUT = Path(r"C:/Users/Orange/workspace/curve-site/_g2")
OUT.mkdir(exist_ok=True)

doc = pymupdf.open(PDF)
print(f"{len(doc)} صفحة\n")
print(f"{'ص':>3} {'المساحة الأكبر (خلفية)':>26} {'114؟':>6} {'أسود%':>7} {'رمادي فاتح%':>11}  ألوان بارزة")
rows = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    img = Path(OUT) / f"p{i+1:02d}.png"
    pix.save(img)
    a = np.asarray(Image.open(img).convert("RGB")).reshape(-1, 3)
    total = len(a)
    cnt = Counter(map(tuple, a[::7]))                      # عيّنة سريعة
    top = cnt.most_common(1)[0][0]
    def frac(rgb, tol=6):
        m = (np.abs(a.astype(int) - np.array(rgb)).max(axis=1) <= tol)
        return 100.0 * m.sum() / total
    f114, f0 = frac((114, 114, 114)), frac((0, 0, 0))
    grays = [c for c, n in cnt.most_common(6) if max(c) - min(c) < 8]
    rows.append((i + 1, top, f114, f0, grays, str(img)))
    print(f"{i+1:>3} {str(top):>26} {f114:>5.1f}% {f0:>6.1f}% {len(grays):>11}  {grays[:5]}")

print("\n=== الصفحات اللي فيها #727272 بنسبة معتبرة ===")
for n, top, f114, f0, grays, path in rows:
    if f114 > 3:
        print(f"  ص{n:02d}: #727272 = {f114:.1f}% من الصفحة · أسود = {f0:.1f}% · ملف: {path}")
