"""Stage 3: brand imagery (monochrome) + RB font wiring (files pending)."""
import io, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(ROOT, "styles.css")
FONTS = os.path.join(ROOT, "assets", "fonts")
os.makedirs(FONTS, exist_ok=True)

css = io.open(CSS, encoding="utf-8").read()

css += """

/* --- BRAND IMAGERY: achromatic, motion-led (guideline p.16) ---------------- */
/* brand photography is rendered achromatic everywhere; the portfolio keeps its
   colour available on hover so the client's own work still reads at full impact */
.hero-bg-img { filter: grayscale(1) contrast(1.1) brightness(0.9); }
.about-img { filter: grayscale(1) contrast(1.05); }
.stats-bg-img { filter: grayscale(1) contrast(1.2); }

.work-img {
  filter: grayscale(1) contrast(1.04);
  transition: filter 0.45s var(--ease-out), transform 0.8s var(--ease-out);
}
.work-card:hover .work-img,
.work-card:focus-within .work-img {
  filter: grayscale(0) contrast(1);
}
@media (hover: none) {
  .work-card:hover .work-img { filter: grayscale(1) contrast(1.04); }
}

/* --- TYPOGRAPHY: RB (Arabic) — the approved Arabic family ------------------
   The guideline's RB files were never handed over; these declarations are ready
   and take effect the moment the woff2 files are dropped in assets/fonts/.
   Until then the stack falls back to Cairo, so nothing breaks. */
@font-face {
  font-family: 'RB';
  src: url('assets/fonts/RB-Light.woff2') format('woff2'),
       url('assets/fonts/RB-Light.woff') format('woff'),
       url('assets/fonts/RB-Light.otf') format('opentype');
  font-weight: 300;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'RB';
  src: url('assets/fonts/RB-Regular.woff2') format('woff2'),
       url('assets/fonts/RB-Regular.woff') format('woff'),
       url('assets/fonts/RB-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'RB';
  src: url('assets/fonts/RB-Bold.woff2') format('woff2'),
       url('assets/fonts/RB-Bold.woff') format('woff'),
       url('assets/fonts/RB-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
"""

io.open(CSS, "w", encoding="utf-8").write(css)
print("[css] brand imagery + RB @font-face blocks appended")

readme = """assets/fonts/ — خطوط هوية CURVE
=================================

حسب «CURVE BRAND GUIDELINE» (صفحة 17):

  • اللاتيني : Poppins  — يُحمَّل من Google Fonts (لا حاجة لملفات محلية)
  • العربي   : RB family — Light / Regular / Medium / SemiBold / Bold

الملفات المطلوبة هنا (بنفس الأسماء بالضبط، woff2 مفضّل):

    RB-Light.woff2      (وزن 300)
    RB-Regular.woff2    (وزن 400)
    RB-Medium.woff2     (وزن 500)
    RB-SemiBold.woff2   (وزن 600)
    RB-Bold.woff2       (وزن 700)

تعليمات CSS جاهزة في نهاية styles.css (@font-face باسم العائلة 'RB'، وقد استُبدلت
قبلها Poppins ثم Cairo كبديل). بمجرد وضع الملفات هنا يعمل الخط تلقائياً بلا أي تعديل كود.

ملاحظة: الخطوط المضمّنة داخل ملف الدليل (PDF) هي مجموعات ناقصة (subsets) لا تكفي
لصفحة ويب — يجب الحصول عليها من مصمّم الهوية أو من المكتبة الأصلية.
"""
io.open(os.path.join(FONTS, "README.txt"), "w", encoding="utf-8").write(readme)
print("[fonts] assets/fonts/README.txt written")

# Arabic must stay hidden per the user's instruction
js = io.open(os.path.join(ROOT, "script.js"), encoding="utf-8").read()
flag = "const ARABIC_ENABLED = false;" in js
print(f"[check] ARABIC_ENABLED = false  ->  {'OK (Arabic stays hidden)' if flag else 'WARNING: not found!'}")
