"""Re-apply the hero artwork swap to a clean index.html (the earlier attempt corrupted the
file: a local variable named `h` shadowed the HTML string inside an f-string)."""
import pathlib

R = pathlib.Path(r"C:/Users/Orange/workspace/curve-site")
HTML = R / "index.html"
IMG_W, IMG_H = 1533, 739

doc = HTML.read_text(encoding="utf-8")
assert doc.count("<main>") == 1, "index.html is not the clean single-<main> version"

old_block = '''        <h1 class="hero-title reveal" data-delay="100">
          <span class="title-outline" data-i18n="hero_title_1">IGNITE</span>
          <span class="title-solid" data-i18n="hero_title_2">THE MOTION.</span>
        </h1>'''

new_block = (
    '        <h1 class="hero-title hero-title-art reveal" data-delay="100">\n'
    f'          <img src="assets/web/hero-in-motion.png" class="hero-art"\n'
    f'               alt="CURVE — Ignite the motion" width="{IMG_W}" height="{IMG_H}" loading="eager">\n'
    '          <span class="sr-only">IGNITE THE MOTION.</span>\n'
    '        </h1>'
)

assert old_block in doc, "hero headline block not found verbatim"
doc = doc.replace(old_block, new_block)
HTML.write_text(doc, encoding="utf-8")

check = HTML.read_text(encoding="utf-8")
print("✓ استبدال الهيرو تمّ")
print("   <main> ×", check.count("<main>"), "· </main> ×", check.count("</main>"))
print("   <h1 ×", check.count("<h1"), "· </h1> ×", check.count("</h1>"))
print("   hero-art ×", check.count("hero-art"), "· sr-only ×", check.count("sr-only"))
print("   سطر الصورة:", [l.strip() for l in check.splitlines() if "hero-in-motion" in l])
