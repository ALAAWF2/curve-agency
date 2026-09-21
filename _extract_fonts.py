"""Extract the fonts embedded in the CURVE brand guideline and read their identity."""
import os
import pymupdf
from fontTools.ttLib import TTFont

PDF = r"C:\Users\Orange\AppData\Local\hermes\cache\documents\doc_4354fb3c6a22_CURVE BRAND GUIDELINE.pdf"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_guideline_fonts")
os.makedirs(OUT, exist_ok=True)

doc = pymupdf.open(PDF)
seen = {}
for pno, page in enumerate(doc):
    for f in page.get_fonts(full=True):
        xref, ext, ftype, basefont, name, enc = f[0], f[1], f[2], f[3], f[4], f[5]
        if basefont not in seen:
            seen[basefont] = (xref, ext, ftype, pno + 1)

print(f"عدد الخطوط المضمّنة الفريدة: {len(seen)}\n")
for base, (xref, ext, ftype, first_page) in sorted(seen.items()):
    path = None
    try:
        name, fext, ftype2, buf = doc.extract_font(xref)
        if buf:
            path = os.path.join(OUT, f"{name}.{fext}")
            open(path, "wb").write(buf)
    except Exception as e:  # noqa: BLE001
        print(f"  {base}: تعذّر الاستخراج ({e})")
        continue

    info = {}
    try:
        ft = TTFont(path, lazy=True)
        names = {}
        for rec in ft["name"].names:
            try:
                names.setdefault(rec.nameID, rec.toUnicode())
            except Exception:  # noqa: BLE001
                pass
        for nid, label in [(1, "family"), (2, "style"), (4, "full"), (5, "version"), (6, "ps"),
                           (8, "manufacturer"), (9, "designer"), (10, "description"),
                           (11, "vendorURL"), (13, "license"), (14, "licenseURL"),
                           (16, "familyRegistered"), (17, "styleRegistered")]:
            if nid in names:
                info[label] = names[nid].strip()[:150]
        info["glyphs"] = ft["maxp"].numGlyphs if "maxp" in ft else "?"
        try:
            cmap = ft.getBestCmap()
            info["cmap_codepoints"] = len(cmap)
            info["arabic_range"] = sum(1 for c in cmap if 0x0600 <= c <= 0x06FF)
        except Exception:  # noqa: BLE001
            pass
        info["is_subset"] = "subset" if any(k in info.get("full", "") for k in ("Subset", "subset")) or (info.get("glyphs", 999) < 200) else "full?"
        ft.close()
    except Exception as e:  # noqa: BLE001
        info["read_error"] = str(e)

    print(f"── {base}  (صفحة {first_page}, {ext}, {ftype}) · ملف: {os.path.basename(path) if path else '-'}")
    for k, v in info.items():
        print(f"     {k:16s}: {v}")
    print()
