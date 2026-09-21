
import io, re
ROOT = r"C:/Users/Orange/workspace/curve-site"
HTML, JS = ROOT + "/index.html", ROOT + "/script.js"

html = io.open(HTML, encoding="utf-8").read()
new_ul = ('<ul class="mobile-nav-links">\n'
 '        <li><a href="#work" class="mobile-nav-link" data-i18n="nav_work">WORK</a></li>\n'
 '        <li><a href="#services" class="mobile-nav-link" data-i18n="nav_services">SERVICES</a></li>\n'
 '        <li><a href="#about" class="mobile-nav-link" data-i18n="nav_about">PROFILE</a></li>\n'
 '        <li><a href="#contact" class="mobile-nav-link" data-i18n="nav_contact">CONTACT</a></li>\n'
 '      </ul>')
html, n = re.subn(r'<ul class="mobile-nav-links">.*?</ul>', new_ul, html, flags=re.S)
io.open(HTML, "w", encoding="utf-8").write(html)
print(f"mobile menu: {n} list(s) reduced to 4 items")

js = io.open(JS, encoding="utf-8").read()
before = js
# the i18n dictionary rewrites nav labels on load -> align the EN strings with the new nav
for key, val in (("nav_work", "WORK"), ("nav_about", "PROFILE")):
    js = re.sub(r'(' + key + r'\s*:\s*)\'[^\']*\'', lambda m: m.group(1) + "'" + val + "'", js, count=1)
io.open(JS, "w", encoding="utf-8").write(js)
print("script.js:", "nav_work/nav_about EN labels updated" if js != before else "no change")
for k in ("nav_work", "nav_about", "nav_services", "nav_contact"):
    mm = re.search(k + r"\s*:\s*'([^']*)'", js)
    print(f"   {k:14s} = {mm.group(1) if mm else '-'}")
