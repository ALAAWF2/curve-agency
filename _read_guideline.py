import json, re, sys, collections
import fitz  # pymupdf

PDF = r"C:\Users\Orange\AppData\Local\hermes\cache\documents\doc_4354fb3c6a22_CURVE BRAND GUIDELINE.pdf"
doc = fitz.open(PDF)
print(f"عدد الصفحات: {doc.page_count}")
print(f"مقاس الصفحة: {doc[0].rect}")

all_text = []
for i, page in enumerate(doc):
    t = page.get_text().strip()
    all_text.append(f"\n===== صفحة {i+1} =====\n{t}")
    if i < 6:
        print(f"\n--- صفحة {i+1} (نص {len(t)} حرف) ---")
        print(t[:700])

full = "\n".join(all_text)
open(r"C:/Users/Orange/workspace/curve-site/_guideline_text.txt", "w", encoding="utf-8").write(full)
print("\n[✓] النص الكامل محفوظ: curve-site/_guideline_text.txt")

# hex colors mentioned in text
hexes = collections.Counter(re.findall(r"#?([0-9A-Fa-f]{6})\b", full))
cand = [h.upper() for h, c in hexes.most_common(40) if re.search(r"[A-Fa-f]", h)]
print("\nأكواد ألوان محتملة بالنص:", cand[:25])

# fonts embedded
fonts = collections.Counter()
for page in doc:
    for f in page.get_fonts():
        fonts[f[3]] += 1
print("\nالخطوط المضمّنة بالـPDF:", dict(fonts))

# images info
imgs = 0
for page in doc:
    imgs += len(page.get_images(full=True))
print("عدد الصور المضمّنة:", imgs)

# sample dominant colors per page (render small, count pixels)
print("\nألوان سائدة لكل صفحة (أول 12 صفحة):")
for i in range(min(12, doc.page_count)):
    pix = doc[i].get_pixmap(matrix=fitz.Matrix(0.25, 0.25))
    data = pix.samples
    n = pix.width * pix.height
    cnt = collections.Counter()
    step = pix.n
    for p in range(0, len(data), step * 7):  # every 7th px
        cnt[data[p:p+3].hex().upper()] += 1
    top = [f"#{c} {round(v*100/max(1,n/7))}%" for c, v in cnt.most_common(4)]
    print(f"  ص{i+1:02d}: " + " · ".join(top))
