"""Fix: the ::after rule lost its quotes (content: ;) so the pattern never painted."""
import io, re

ROOT = r"C:/Users/Orange/workspace/curve-site"
CSS = ROOT + "/styles.css"
DOC = ROOT + "/BRAND_COMPLIANCE.md"

css = io.open(CSS, encoding="utf-8").read()
before = css

css = css.replace('  content: ;\n  position: absolute;\n  inset: -35%;',
                  '  content: "";\n  position: absolute;\n  inset: -35%;')
css = css.replace('  opacity: 0.085;\n  transform: rotate(45deg);',
                  '  opacity: 0.13;   /* measured against the pixel data: 0.085 read as flat white */\n  transform: rotate(45deg);')
assert 'content: "";' in css and 'opacity: 0.13;' in css, "css fix did not apply"
io.open(CSS, "w", encoding="utf-8").write(css)
print("[css] ::after content restored + opacity 0.13")

doc = io.open(DOC, encoding="utf-8").read()
doc = doc.replace("22|5. **أسطح مسطّحة**", "5. **أسطح مسطّحة**")
doc = doc.replace("24:6. **حالات النموذج**", "7. **حالات النموذج**")
doc = doc.replace("6. **حالات النموذج**", "7. **حالات النموذج**")
io.open(DOC, "w", encoding="utf-8").write(doc)
print("[doc] stray line-number prefix fixed, numbering cleaned")
print("      chars:", len(before), "->", len(css))
