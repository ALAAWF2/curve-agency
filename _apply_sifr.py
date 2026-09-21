"""SIFR alignment (items 1-6) applied to the CURVE site.

Reference: SIFR GROUP (live captures in reference_sifr_live/) — borrowed: structure,
type scale, whitespace, rhythm. NOT borrowed: the red accent (CURVE's brand guideline
allows black/white/opacity tints only).
"""
import io, re, shutil

ROOT = r"C:/Users/Orange/workspace/curve-site"
HTML = ROOT + "/index.html"
CSS = ROOT + "/styles.css"

shutil.copy(HTML, ROOT + "/_bak2_index.html")
shutil.copy(CSS, ROOT + "/_bak2_styles.css")

html = io.open(HTML, encoding="utf-8").read()
report = []

# ---------------------------------------------------------------- 1) nav -> 4 items
NAV_ITEMS = [
    ("#work", "nav_work", "WORK"),
    ("#services", "nav_services", "SERVICES"),
    ("#about", "nav_about", "PROFILE"),
    ("#contact", "nav_contact", "CONTACT"),
]
new_ul = '<ul class="nav-links">\n' + "\n".join(
    f'          <li><a href="{href}" class="nav-link" data-i18n="{key}">{label}</a></li>'
    for href, key, label in NAV_ITEMS) + "\n        </ul>"

n_uls = len(re.findall(r'<ul class="nav-links">.*?</ul>', html, re.S))
html = re.sub(r'<ul class="nav-links">.*?</ul>', new_ul, html, flags=re.S)
report.append(f"nav: replaced {n_uls} nav list(s) with 4 items")

# ------------------------------------------------- 2) section eyebrows: drop "NN / "
def strip_idx(m):
    return f'<div class="section-idx{ m.group(1) or "" }">' + m.group(3)

html, n_idx = re.subn(r'<div class="section-idx([^"]*)">\s*\d{2}\s*/\s*(<span[^>]*>)',
                      lambda m: f'<div class="section-idx{m.group(1)}">{m.group(2)}', html)
report.append(f"section eyebrows: removed numeric prefixes from {n_idx} section(s)")

# ------------------------------------- 4) work badge out of the image, into the caption
def fix_card(block: str) -> str:
    m = re.search(r'<div class="work-badge"([^>]*)>(.*?)</div>', block, re.S)
    if not m:
        return block
    badge = f'<div class="work-badge"{m.group(1)}>{m.group(2)}</div>'
    block = block.replace(m.group(0), "")            # remove from over the image
    block = block.replace('<div class="work-info">', f'<div class="work-info">\n            {badge}', 1)
    return block

cards = re.findall(r'<article class="work-card".*?</article>', html, re.S)
for c in cards:
    html = html.replace(c, fix_card(c))
report.append(f"work badges: moved into the caption for {len(cards)} cards")

# ------------------------------------------------- 5) flag the contact section for inversion
html, n_contact = re.subn(r'(<section class="section contact-section") id="contact"',
                          r'\1 id="contact" data-ground="light"', html)
report.append(f"contact section: flagged for light inversion ({n_contact})")

io.open(HTML, "w", encoding="utf-8").write(html)

# ---------------------------------------------------------------- CSS
css = io.open(CSS, encoding="utf-8").read()

css += """

/* ==========================================================================
   SIFR ALIGNMENT — 21 Sep 2026 (reference: sifrprofile.com + CURVE guideline PDF)
   Borrowed from the reference: 4-item nav · label-only section markers · much larger
   display type with tighter leading · plain-text filters · image-first, borderless,
   staggered work grid · a fully inverted contact section · ~190px type margins.
   NOT borrowed: the reference's chromatic accent — the CURVE guideline allows only
   black, white and opacity tints, so every emphasis is black/white contrast.
   ========================================================================== */

:root {
  --container-pad: clamp(1.5rem, 9.2vw, 11.875rem);   /* reference margin: 190px @1920 */
  --section-pad-y: clamp(6rem, 13vw, 13rem);
}

/* --- type scale ---------------------------------------------------------- */
.hero-title {
  font-size: clamp(3.4rem, 11.4vw, 13rem);   /* reference hero: 205-225px @1920 */
  line-height: 0.88;
  letter-spacing: -0.04em;
}

.section-headline {
  font-size: clamp(2.4rem, 5.7vw, 7rem);     /* reference section type: 96-104px @1920 */
  line-height: 0.92;
  letter-spacing: -0.03em;
  max-width: 1200px;
}

.section-idx {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: var(--text-muted);
  margin-bottom: 1.75rem;
}

.section-desc { max-width: 780px; }

/* --- filters: plain text, no containers ---------------------------------- */
.filter-btn {
  background: transparent;
  border: 0;
  border-radius: 0;
  padding: 0.15rem 0;
  color: var(--text-dim);
  font-size: 0.72rem;
  letter-spacing: 0.18em;
}
.filter-btn:hover { color: var(--text-pure); border: 0; }
.filter-btn.active {
  background: transparent;
  border: 0;
  color: var(--accent);
}
.work-filters { gap: clamp(1rem, 2.4vw, 2.25rem); }

/* --- work grid: image first, no frames, staggered rhythm ----------------- */
.work-visual {
  border: 0;
  border-radius: 0;
  background-color: transparent;
  aspect-ratio: 16 / 9;                       /* reference uses a cinematic ratio */
  margin-bottom: 1.75rem;
}
.work-card {
  background: transparent;
  border: 0;
  border-radius: 0;
}
.work-info { display: flex; flex-direction: column; gap: 0.45rem; }

/* the category label now sits under the image, as plain type */
.work-badge {
  position: static;
  inset: auto;
  display: inline-block;
  background: transparent;
  border: 0;
  border-radius: 0;
  padding: 0;
  color: var(--text-dim);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.work-client { color: var(--text-pure); }
.work-title { margin-top: 0.15rem; }

@media (min-width: 900px) {
  .work-grid > .work-card:nth-child(even) { margin-top: clamp(2.5rem, 5vw, 5rem); }
  .work-grid { gap: clamp(2rem, 3vw, 3.25rem) clamp(1.5rem, 2vw, 2rem); }
}

/* --- contact section: full inversion to the light ground (reference device,
       executed in black/white instead of the reference's colour) ---------- */
.contact-section[data-ground="light"] {
  position: relative;
  background-color: var(--paper);
  color: #000000;
  overflow: hidden;
}
.contact-section[data-ground="light"]::before {
  content: "";
  position: absolute;
  inset: -25% -10%;
  z-index: 0;
  pointer-events: none;
  background-image: url("assets/curve-pattern-dark.svg");
  background-size: 120px 120px;
  opacity: 0.06;
  transform: rotate(45deg);
}
.contact-section[data-ground="light"] > .container { position: relative; z-index: 1; }

.contact-section[data-ground="light"] .section-idx,
.contact-section[data-ground="light"] .contact-lead,
.contact-section[data-ground="light"] .detail-label,
.contact-section[data-ground="light"] .social-label,
.contact-section[data-ground="light"] .form-desc { color: rgba(0, 0, 0, 0.62); }
.contact-section[data-ground="light"] .section-idx::after { background-color: rgba(0, 0, 0, 0.18); }
.contact-section[data-ground="light"] .detail-val,
.contact-section[data-ground="light"] .detail-val.direct-link { color: #000000; }
.contact-section[data-ground="light"] .title-outline {
  -webkit-text-stroke-color: rgba(0, 0, 0, 0.45);
  color: transparent;
}
.contact-section[data-ground="light"] .title-solid { color: #000000; }
.contact-section[data-ground="light"] .contact-details-list,
.contact-section[data-ground="light"] .contact-detail-item { border-color: rgba(0, 0, 0, 0.12); }
.contact-section[data-ground="light"] .social-btn {
  border-color: rgba(0, 0, 0, 0.22);
  color: rgba(0, 0, 0, 0.8);
  background: transparent;
}
.contact-section[data-ground="light"] .social-btn:hover {
  border-color: #000000;
  color: #000000;
}
.contact-section[data-ground="light"] .form-container {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.12);
}
.contact-section[data-ground="light"] .form-title { color: #000000; }
.contact-section[data-ground="light"] .form-group label { color: rgba(0, 0, 0, 0.6); }
.contact-section[data-ground="light"] .form-group input,
.contact-section[data-ground="light"] .form-group select,
.contact-section[data-ground="light"] .form-group textarea {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.18);
  color: #000000;
}
.contact-section[data-ground="light"] .form-group input::placeholder,
.contact-section[data-ground="light"] .form-group textarea::placeholder { color: rgba(0, 0, 0, 0.35); }
.contact-section[data-ground="light"] .form-group input:focus,
.contact-section[data-ground="light"] .form-group select:focus,
.contact-section[data-ground="light"] .form-group textarea:focus {
  border-color: #000000;
  outline: 2px solid rgba(0, 0, 0, 0.18);
  outline-offset: 1px;
}
.contact-section[data-ground="light"] .form-group select { color: #000000; }
.contact-section[data-ground="light"] .form-group select option { background: #ffffff; color: #000000; }
.contact-section[data-ground="light"] .form-status-box {
  border-color: rgba(0, 0, 0, 0.25) !important;
  background: rgba(0, 0, 0, 0.05) !important;
  color: #000000 !important;
}
.contact-section[data-ground="light"] .form-err-msg { color: rgba(0, 0, 0, 0.75); }
.contact-section[data-ground="light"] .btn-primary {
  background-color: #000000;
  border-color: #000000;
  color: #ffffff;
}
.contact-section[data-ground="light"] .btn-primary:hover {
  background-color: rgba(0, 0, 0, 0.85);
  border-color: rgba(0, 0, 0, 0.85);
  color: #ffffff;
}
"""

io.open(CSS, "w", encoding="utf-8").write(css)

print("\n".join("  ✓ " + r for r in report))
print(f"  ✓ css: SIFR alignment block appended ({len(css)} chars total)")
