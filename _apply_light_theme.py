"""Apply the approved light theme to the CURVE site.

Source of truth (measured, not guessed):
  * CURVE BRAND GUIDELINE (1).pdf, page 23 (website mockup): ground #EDEDED ~86% of pixels,
    black type, #727272 as the secondary grey (0.58%)
  * #727272 == the guideline's 55% tint of black (255*0.45 = 114.75)
  * Alaa approved the rendered variant "B" (#EDEDED ground, #727272 secondary text)

Strategy: flip the design tokens, map the hard-coded white-on-dark literals to black-on-light,
then override the few surfaces that are not token-driven (header, hero veil, footer, mobile
menu, pattern band, partner cells) and invert the white logo/partner art with CSS filters.
"""
import pathlib, re, shutil, datetime

ROOT = pathlib.Path(r"C:/Users/Orange/workspace/curve-site")
CSS = ROOT / "styles.css"
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(CSS, ROOT / f"_bak_light_styles_{stamp}.css")

css = CSS.read_text(encoding="utf-8")
log = []

# ---------------------------------------------------------------- 1) tokens
TOKENS = {
    "--bg-dark: #000000;":            "--bg-dark: #EDEDED;            /* approved light ground */",
    "--bg-surface: rgba(255, 255, 255, 0.04);": "--bg-surface: rgba(0, 0, 0, 0.02);",
    "--bg-card: rgba(255, 255, 255, 0.05);":    "--bg-card: rgba(255, 255, 255, 0.65);",
    "--bg-card-hover: rgba(255, 255, 255, 0.085);": "--bg-card-hover: #E5E5E5;",
    "--border-dim: rgba(255, 255, 255, 0.10);":   "--border-dim: rgba(0, 0, 0, 0.12);",
    "--border-light: rgba(255, 255, 255, 0.20);": "--border-light: rgba(0, 0, 0, 0.22);",
    "--border-hover: rgba(255, 255, 255, 0.45);": "--border-hover: rgba(0, 0, 0, 0.55);",
    "--text-pure: #ffffff;":          "--text-pure: #000000;",
    "--text-primary: rgba(255, 255, 255, 0.90);": "--text-primary: #000000;",
    "--text-muted: rgba(255, 255, 255, 0.55);":   "--text-muted: #727272;    /* guideline 55% tint */",
    "--paper: #eceaea;":              "--paper: #EDEDED;            /* aligned with the mockup ground */",
    "--ink: #000000;":                "--ink: #000000;",
    "--accent: #ffffff;":             "--accent: #000000;",
}
for a, b in TOKENS.items():
    if a in css:
        css = css.replace(a, b)
        log.append(f"token  {a.split(':')[0]:22s} -> {b.split(':')[1].strip()[:34]}")
    else:
        log.append(f"token  {a.split(':')[0]:22s} !! not found verbatim")

# text-dim may have a different alpha — handle by regex
css, n = re.subn(r"--text-dim:\s*rgba\(255,\s*255,\s*255,\s*[0-9.]+\);", "--text-dim: #727272;", css)
log.append(f"token  --text-dim replaced × {n}")

# ---------------------------------------------- 2) remaining white-on-dark literals
MAP = {  # alpha -> replacement (surfaces get subtler, borders/text keep their weight)
    "0.02": "0.02", "0.03": "0.03", "0.04": "0.03", "0.05": "0.04", "0.08": "0.05",
    "0.085": "0.06", "0.1": "0.12", "0.10": "0.12", "0.12": "0.14", "0.14": "0.16",
    "0.20": "0.22", "0.30": "0.30", "0.32": "0.32", "0.45": "0.5", "0.55": "0.55",
    "0.65": "0.72", "0.86": "0.86", "0.90": "1", "0.92": "1",
}
def swap(m):
    a = m.group(1)
    new = MAP.get(a)
    if new is None:
        return m.group(0)
    return f"rgba(0, 0, 0, {new})"
css, n = re.subn(r"rgba\(255,\s*255,\s*255,\s*([0-9.]+)\)", swap, css)
log.append(f"literals rgba(255,255,255,a) rewritten × {n}")

# ------------------------------------------------- 3) non-token surfaces
OVERRIDES = """

/* ==========================================================================
   LIGHT THEME — 22 Sep 2026 · approved by Alaa ("هيك ممتاز")
   Ground #EDEDED, black headings, #727272 secondary text — taken from the website
   mockup on page 23 of CURVE BRAND GUIDELINE (1).pdf (measured: #EDEDED = 86% of
   the mockup pixels, #727272 = its grey type, which is the guideline's 55% tint).
   Everything stays grayscale: no chromatic value is introduced anywhere.
   ========================================================================== */
.site-header { background-color: transparent; }
.site-header.scrolled {
  background-color: rgba(237, 237, 237, 0.92);
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.hero-overlay {
  background: linear-gradient(180deg, rgba(237, 237, 237, 0.45) 0%, rgba(237, 237, 237, 0.86) 68%, #EDEDED 100%);
}
.hero-bg-img { filter: grayscale(1) contrast(1.06) brightness(1.04); }
.site-footer { background-color: #E5E5E5; }
.mobile-menu { background-color: rgba(237, 237, 237, 0.98); }
.brand-band { background-color: #E5E5E5; background-image: url("assets/curve-pattern-dark.svg"); }
.partner-cell { background-color: #EDEDED; }
.partner-cell:hover { background-color: #E5E5E5; }
/* white logo/partner art on a dark ground must read as black on the light ground */
.logo-img, .footer-logo, .brand-logo img { filter: invert(1) grayscale(1); }
.partner-cell img { filter: invert(1) grayscale(1) opacity(0.72); transition: opacity var(--transition-fast); }
.partner-cell:hover img { opacity: 1; }
.logo-img.logo-light { opacity: 1; }
/* the contact section is no longer a special case — the whole site is light */
.contact-section[data-ground="light"] { background-color: #EDEDED; }
.contact-section[data-ground="light"]::before { opacity: 0.05; }
::-webkit-scrollbar-track { background: #E5E5E5; }
::-webkit-scrollbar-thumb { background: rgba(0, 0, 0, 0.28); }
::selection { background: #000000; color: #EDEDED; }
"""

css += OVERRIDES
CSS.write_text(css, encoding="utf-8")
print("\n".join(log))
print(f"\n✓ styles.css updated ({CSS.stat().st_size} بايت) · نسخة احتياطية: _bak_light_styles_{stamp}.css")
