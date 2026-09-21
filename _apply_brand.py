"""Apply the CURVE BRAND GUIDELINE (27-page deck) to the website.

Rules extracted from the deck:
  * COLOR SYSTEM  -> black #000000 only, + white and black-opacity tints (10-90%). NO chromatic accent.
  * TYPOGRAPHY    -> Latin: Poppins (ExtraLight..ExtraBold) · Arabic: RB family (Light/Bold) [files not supplied -> Cairo fallback]
  * LOGO          -> min web size 120 x 29.873 px · keep aspect (no distortion) · icon mark (the R) for favicon/small formats
                     · clear space 1X · keyline stroke >= 2px digital · no frame, no rotation
  * PATTERN       -> 4 motifs (rosette / double-hook / spandrel / 4-petal) built from straight edges + arcs of one radius,
                     solid black fills, tiled on a 45-deg diagonal square lattice with constant white channels
  * TONE          -> adaptive · conversational · proactive · smooth · confident · innovative
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(ROOT, "styles.css")
HTML = os.path.join(ROOT, "index.html")
ASSETS = os.path.join(ROOT, "assets")

# ---------------------------------------------------------------- 1) pattern SVG
def pattern_svg(ink: str) -> str:
    """Seamless tile: centre rosette + 4 corner spandrels + edge hooks on a square unit."""
    T = 88          # tile size
    r = 22          # single radius used by every arc
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}">
  <defs>
    <!-- one blade: straight edges + concave quarter arc of radius {r} -->
    <path id="blade" d="M0 0 L{r} 0 A{r} {r} 0 0 0 0 {r} Z" fill="{ink}"/>
    <path id="petal" d="M0 0 L{r} 0 A{r} {r} 0 0 0 0 {r} Z" fill="{ink}"/>
    <g id="rosette">
      <use href="#blade"/>
      <use href="#blade" transform="rotate(90)"/>
      <use href="#blade" transform="rotate(180)"/>
      <use href="#blade" transform="rotate(270)"/>
    </g>
    <g id="petal4">
      <use href="#petal"/>
      <use href="#petal" transform="rotate(45)"/>
      <use href="#petal" transform="rotate(90)"/>
      <use href="#petal" transform="rotate(135)"/>
      <use href="#petal" transform="rotate(180)"/>
      <use href="#petal" transform="rotate(225)"/>
      <use href="#petal" transform="rotate(270)"/>
      <use href="#petal" transform="rotate(315)"/>
    </g>
    <!-- spandrel: square corner block minus its inscribed quarter disc -->
    <path id="spandrel" d="M0 0 L{r} 0 A{r} {r} 0 0 1 0 {r} Z" fill="{ink}"/>
  </defs>
  <g>
    <!-- centre rosette -->
    <use href="#rosette" x="{T/2}" y="{T/2}" transform="translate({T/2},{T/2}) translate(-{r},-{r})"/>
    <!-- corner markers (half-rosettes at the 4 corners keep the tile seamless) -->
    <use href="#rosette" transform="translate(0,0) translate(-{r},-{r})"/>
    <use href="#rosette" transform="translate({T},0) translate(-{r},-{r})"/>
    <use href="#rosette" transform="translate(0,{T}) translate(-{r},-{r})"/>
    <use href="#rosette" transform="translate({T},{T}) translate(-{r},-{r})"/>
    <!-- edge hooks: mirrored pairs, point-symmetric about the edge midpoint -->
    <g transform="translate({T/2},0)">
      <use href="#spandrel" transform="rotate(180) translate(-{r/2},0)"/>
    </g>
    <g transform="translate(0,{T/2})">
      <use href="#spandrel" transform="translate(0,-{r/2})"/>
    </g>
    <!-- interstitial 4-petal pinwheel, rotated 45 deg -->
    <use href="#petal4" transform="translate({T/2},{T/2}) translate(-{r*0.75},-{r*0.75}) scale(0.75)"/>
  </g>
</svg>
"""

open(os.path.join(ASSETS, "curve-pattern.svg"), "w", encoding="utf-8").write(pattern_svg("#FFFFFF"))
open(os.path.join(ASSETS, "curve-pattern-dark.svg"), "w", encoding="utf-8").write(pattern_svg("#000000"))
print("[1] assets/curve-pattern.svg + curve-pattern-dark.svg")

# ---------------------------------------------------------------- 2) styles.css
css = io.open(CSS, encoding="utf-8").read()
orig = css

TOKENS_OLD = """  /* Colors */
  --bg-dark: #08080a;
  --bg-surface: #111115;
  --bg-card: #15151b;
  --bg-card-hover: #1c1c24;
  --border-dim: rgba(255, 255, 255, 0.07);
  --border-light: rgba(255, 255, 255, 0.15);
  --border-hover: rgba(255, 255, 255, 0.35);
  
  --text-pure: #ffffff;
  --text-primary: #f2f2f4;
  --text-muted: #8e8e98;
  --text-dim: #5a5a64;

  --accent: #ff3b30;
  --accent-glow: rgba(255, 59, 48, 0.25);
  --accent-hover: #ff5547;

  /* Typography */
  --font-display: 'Syne', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-arabic-display: 'Tajawal', 'IBM Plex Sans Arabic', sans-serif;
  --font-arabic-sans: 'IBM Plex Sans Arabic', 'Tajawal', sans-serif;"""

TOKENS_NEW = """  /* Colors — CURVE BRAND GUIDELINE: black #000000 + white + black/white opacity tints only.
     No chromatic accent is approved anywhere in the visual identity. */
  --bg-dark: #000000;
  --bg-surface: rgba(255, 255, 255, 0.04);
  --bg-card: rgba(255, 255, 255, 0.05);
  --bg-card-hover: rgba(255, 255, 255, 0.085);
  --border-dim: rgba(255, 255, 255, 0.10);
  --border-light: rgba(255, 255, 255, 0.20);
  --border-hover: rgba(255, 255, 255, 0.45);

  --paper: #eceaea;            /* approved light ground */
  --ink: #000000;              /* approved ink */
  --text-pure: #ffffff;
  --text-primary: rgba(255, 255, 255, 0.90);
  --text-muted: rgba(255, 255, 255, 0.55);
  --text-dim: rgba(255, 255, 255, 0.32);

  /* the "accent" role is filled by pure black / pure white contrast — not a hue */
  --accent: #ffffff;
  --accent-glow: rgba(255, 255, 255, 0.14);
  --accent-hover: rgba(255, 255, 255, 0.86);

  /* Typography — guideline: Latin = Poppins (7 weights) · Arabic = RB family */
  --font-display: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-arabic-display: 'RB', 'Cairo', 'Poppins', sans-serif;
  --font-arabic-sans: 'RB', 'Cairo', 'Poppins', sans-serif;"""

assert TOKENS_OLD in css, "token block not found"
css = css.replace(TOKENS_OLD, TOKENS_NEW)

REPL = [
    # chromatic -> monochrome
    ("rgba(255, 59, 48, 0.04)", "rgba(255, 255, 255, 0.03)"),
    ("rgba(255, 59, 48, 0.06)", "rgba(255, 255, 255, 0.05)"),
    ("rgba(255, 59, 48, 0.12)", "rgba(255, 255, 255, 0.10)"),
    ("rgba(255, 59, 48, 0.15)", "rgba(255, 255, 255, 0.14)"),
    ("rgba(255, 59, 48, 0.25)", "rgba(255, 255, 255, 0.40)"),
    ("#ff3b30", "#ffffff"),
    ("#ff5547", "#ffffff"),
    ("#2ECC71", "#ffffff"),
    ("#2ecc71", "#ffffff"),
    # neutralise off-blacks / blue-tinted greys to the approved system
    ("rgba(8, 8, 10, 0.88)", "rgba(0, 0, 0, 0.92)"),
    ("rgba(8, 8, 10, 0.82)", "rgba(0, 0, 0, 0.86)"),
    ("rgba(8, 8, 10, 0.8)", "rgba(0, 0, 0, 0.80)"),
    ("rgba(8, 8, 10, 0.4)", "rgba(0, 0, 0, 0.45)"),
    ("rgba(8, 8, 10, 0.9)", "rgba(0, 0, 0, 0.90)"),
    ("rgba(3, 3, 4, 0.6)", "rgba(0, 0, 0, 0.60)"),
    ("rgba(3, 3, 4, 0.95)", "rgba(0, 0, 0, 0.95)"),
    ("rgba(17, 17, 21, 0.75)", "rgba(255, 255, 255, 0.04)"),
    ("#15151e", "#101010"),
    ("#15151b", "#101010"),
    ("#1c1c24", "#151515"),
    ("#111115", "#0b0b0b"),
    ("#08080a", "#000000"),
    ("#f2f2f4", "#f2f2f2"),
    ("#8e8e98", "#8e8e8e"),
    ("#5a5a64", "#5a5a5a"),
    ("#74747C", "#747474"),
    ("#85858D", "#858585"),
    ("#92929A", "#929292"),
    ("#A8A8AB", "#a8a8a8"),
    ("#E8E8EA", "#e8e8e8"),
    ("#E6E6E7", "#e6e6e6"),
    ("#F8F8F8", "#f8f8f8"),
    ("#414144", "#414141"),
    ("#3C3C3F", "#3c3c3c"),
    ("#29292C", "#292929"),
    ("#2A2A2C", "#2a2a2a"),
    ("#39393D", "#393939"),
    ("#1B1B1E", "#1b1b1b"),
    ("#F7F7F7", "#f7f7f7"),
    # flat premium minimalism: drop glows / blur / gradient sheen (guideline = solid fills)
    ("  box-shadow: 0 0 10px var(--accent);\n", ""),
    ("  box-shadow: 0 4px 25px var(--accent-glow);\n", ""),
    ("  backdrop-filter: blur(12px);\n  -webkit-backdrop-filter: blur(12px);\n", ""),
    ("  backdrop-filter: blur(8px);\n  -webkit-backdrop-filter: blur(8px);\n", ""),
    ("  background: linear-gradient(135deg, var(--bg-surface) 0%, #101010 100%);",
     "  background: var(--bg-surface);"),
]
for a, b in REPL:
    css = css.replace(a, b)

# featured service card: express emphasis by inversion (white), not by a hue
css = css.replace(""".service-card.featured-service {
  background: linear-gradient(145deg, var(--bg-surface) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-color: rgba(255, 255, 255, 0.40);
}""", """.service-card.featured-service {
  background: #ffffff;
  border-color: #ffffff;
}""")

io.open(CSS, "w", encoding="utf-8").write(css)
print(f"[2] styles.css updated ({len(orig)} -> {len(css)} chars, {len(REPL)} rule groups)")

# ---------------------------------------------------------------- 3) index.html
html = io.open(HTML, encoding="utf-8").read()
h_orig = html

html = html.replace(
    "family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Syne:wght@500;700;800&family=Tajawal:wght@400;500;700;800;900",
    "family=Poppins:wght@200;300;400;500;600;700;800&family=Cairo:wght@400;600;700")

# favicon: guideline -> the icon mark (the R), not the wordmark
html = html.replace(
    '<link rel="icon" type="image/png" href="assets/curve-logo-white.png">',
    '<link rel="icon" type="image/png" href="assets/curve-mark-dark.png">\n'
    '    <link rel="apple-touch-icon" href="assets/curve-mark-dark.png">')

# footer logo: below the 120px minimum -> raise to 130px, aspect preserved
html = html.replace(
    '<img src="assets/curve-wordmark-white.png" alt="CURVE" class="footer-logo" width="110" height="20" loading="lazy">',
    '<img src="assets/curve-wordmark-white.png" alt="CURVE" class="footer-logo" width="130" loading="lazy">')

io.open(HTML, "w", encoding="utf-8").write(html)
print(f"[3] index.html updated ({len(h_orig)} -> {len(html)} chars)")

# ---------------------------------------------------------------- 4) leftovers
for path, label in ((CSS, "styles.css"), (HTML, "index.html")):
    txt = io.open(path, encoding="utf-8").read()
    bad = []
    for h in set(re.findall(r"#([0-9A-Fa-f]{6})\b", txt)):
        r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
        if max(r, g, b) - min(r, g, b) > 14:
            bad.append("#" + h)
    for m in re.findall(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", txt):
        r, g, b = map(int, m)
        if max(r, g, b) - min(r, g, b) > 14:
            bad.append(f"rgb({r},{g},{b})")
    print(f"    {label}: ألوان غير أحادية متبقية = {bad if bad else 'صفر ✓'}")
