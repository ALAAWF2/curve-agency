"""Revert variant D: remove the ghosted pattern from the featured card (back to plain white inversion)."""
import io, re

CSS = r"C:/Users/Orange/workspace/curve-site/styles.css"
DOC = r"C:/Users/Orange/workspace/curve-site/BRAND_COMPLIANCE.md"

css = io.open(CSS, encoding="utf-8").read()
start = css.find("/* --- FEATURED CARD (variant D")
if start == -1:
    print("[css] block not found — nothing to remove")
else:
    end = css.find(".service-card.featured-service > *", start)
    end = css.find("}", end) + 1
    removed = css[start:end]
    css = css[:start].rstrip() + "\n" + css[end:].lstrip("\n")
    io.open(CSS, "w", encoding="utf-8").write(css)
    print(f"[css] removed {len(removed)} chars of the variant-D block")

leftover = [l for l in css.splitlines() if "curve-pattern-dark" in l or "variant D" in l]
print("[css] leftover lines mentioning the removed pattern:", leftover if leftover else "none ✓")

doc = io.open(DOC, encoding="utf-8").read()
old = [l for l in doc.splitlines() if "البطاقة المميّزة (03 Media Production)" in l]
if old:
    doc = doc.replace(old[0],
        "6. **البطاقة المميّزة (03 Media Production)** — كانت مميّزة بالأصل بالأحمر (حدود + توهج + وسم). بعد منع الألوان صار التمييز **بالقلب فقط: أبيض/أسود** بلا أي نمط داخلها. (جُرِّب إضافة النمط الهندسي داخلها ثم **رُجِع عنه بطلب علاء** 21 أيلول 2026 — «رجعو متل ما كان، ماحبيت».)")
    io.open(DOC, "w", encoding="utf-8").write(doc)
    print("[doc] entry updated to reflect the revert")
