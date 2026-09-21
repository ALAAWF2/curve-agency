"""Stage 2: brand-guideline finishing touches (pattern, inversion, success state)."""
import io, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(ROOT, "styles.css")
HTML = os.path.join(ROOT, "index.html")

css = io.open(CSS, encoding="utf-8").read()

# success state had a green tint -> monochrome (guideline allows no hue)
css = css.replace("background: rgba(46, 204, 113, 0.1);", "background: rgba(255, 255, 255, 0.08);")
css = css.replace("border: 1px solid rgba(46, 204, 113, 0.3);", "border: 1px solid rgba(255, 255, 255, 0.30);")

css += """

/* ==========================================================================
   BRAND GUIDELINE COMPLIANCE — CURVE BRAND GUIDELINE (27 pages)
   · COLOR  : #000000 + white + black/white opacity tints only — no hue anywhere
   · TYPE   : Poppins (Latin, 7 weights) · RB family (Arabic) with Cairo fallback
   · PATTERN: rosette / double-hook / spandrel / 4-petal on a 45deg square lattice,
              arcs of one radius, solid fills, constant-weight channels
   · FLAT   : solid surfaces, hairline rules, no glow, no sheen gradient
   ========================================================================== */

/* --- PATTERN & ELEMENTS (the identity's signature device) ------------------ */
.brand-pattern {
  position: absolute;
  inset: -30%;
  z-index: 0;
  pointer-events: none;
  background-image: url("assets/curve-pattern.svg");
  background-size: 150px 150px;
  background-repeat: repeat;
  opacity: 0.055;
  transform: rotate(45deg);
  transform-origin: center center;
}

.brand-band {
  height: clamp(52px, 7vw, 84px);
  background-color: var(--bg-dark);
  background-image: url("assets/curve-pattern.svg");
  background-size: 68px 68px;
  background-repeat: repeat;
  border-top: 1px solid var(--border-dim);
  border-bottom: 1px solid var(--border-dim);
  opacity: 0.85;
}

.brand-band.invert {
  background-color: var(--paper);
  background-image: url("assets/curve-pattern-dark.svg");
  border-color: rgba(0, 0, 0, 0.12);
}

/* --- LOGO USAGE ----------------------------------------------------------- */
/* min web size 120 x 29.873 px · aspect preserved · no frame · clear space >= 1X */
.brand-logo { padding: 0.25rem 0; }
.logo-img { min-width: 120px; }
.footer-logo { width: 130px; height: auto; }

/* --- FEATURED STATE: emphasis by inversion, not by a hue ------------------ */
.service-card.featured-service,
.service-card.featured-service:hover {
  background: #ffffff;
  border-color: #ffffff;
}
.service-card.featured-service .service-title,
.service-card.featured-service .service-num { color: #000000; }
.service-card.featured-service .service-sub { color: rgba(0, 0, 0, 0.66); }
.service-card.featured-service .service-body { color: rgba(0, 0, 0, 0.68); }
.service-card.featured-service .service-items { border-top-color: rgba(0, 0, 0, 0.15); }
.service-card.featured-service .service-items li { color: rgba(0, 0, 0, 0.70); }
.service-card.featured-service .service-items li::before { color: #000000; }
.service-card.featured-service .service-tag-badge,
.service-card.featured-service .service-tag-badge.highlight {
  background: rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.18);
  color: #000000;
}
"""

io.open(CSS, "w", encoding="utf-8").write(css)
print("[css] compliance block appended")

html = io.open(HTML, encoding="utf-8").read()

if 'class="brand-pattern"' not in html:
    html = html.replace(
        '<div class="hero-overlay"></div>',
        '<div class="hero-overlay"></div>\n        <div class="brand-pattern" aria-hidden="true"></div>', 1)
    print("[html] hero pattern layer added")

if 'class="brand-band"' not in html:
    html = html.replace(
        '<footer class="site-footer">',
        '<!-- brand pattern band (guide: pattern & elements) -->\n'
        '  <div class="brand-band" aria-hidden="true"></div>\n\n'
        '  <footer class="site-footer">', 1)
    print("[html] footer pattern band added")

io.open(HTML, "w", encoding="utf-8").write(html)

import re
for path, label in ((CSS, "styles.css"), (HTML, "index.html")):
    txt = io.open(path, encoding="utf-8").read()
    bad = [f"#{h}" for h in set(re.findall(r"#([0-9A-Fa-f]{6})\b", txt))
           if max(int(h[i:i+2], 16) for i in (0, 2, 4)) - min(int(h[i:i+2], 16) for i in (0, 2, 4)) > 14]
    bad += [f"rgb({m})" for m in re.findall(r"rgba?\((\d+,\s*\d+,\s*\d+)", txt)
            if max(map(int, m.split(','))) - min(map(int, m.split(','))) > 14]
    print(f"[check] {label}: chroma leftovers = {bad if bad else 'ZERO (monochrome OK)'}")
