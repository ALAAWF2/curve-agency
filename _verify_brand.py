#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CURVE - brand-compliance verifier (reusable).

Reads the site files at runtime (never writes them) and checks them against the
rules taken from the client's brand guideline:

  1. Colour      - no chromatic colour in styles.css / index.html.
                   A hex or rgb()/rgba() whose chroma  max(r,g,b)-min(r,g,b)
                   exceeds CHROMA_MAX counts as chromatic and fails.
                   Occurrences inside comments are NOT failures but are always
                   reported separately as "in comment".
  2. Typography  - styles.css font stacks must reference 'Poppins' (Latin) and
                   the Arabic family 'RB'.
  3. Arabic      - script.js must still contain `const ARABIC_ENABLED = false;`
  4. Logo usage  - every <img> with 'logo' in its class must declare a width
                   >= 120px (HTML attribute or CSS rule) and must not hard-code a
                   width/height pair that distorts the asset's real aspect ratio
                   (read from assets/*.png with PIL). Also reports the favicon
                   target and whether it uses the icon mark, not the wordmark.
  5. Assets      - every src/href in index.html starting with 'assets/' exists.
  6. Pattern     - assets/curve-pattern.svg and assets/curve-pattern-dark.svg
                   exist and are referenced from styles.css.

Usage:
    python _verify_brand.py [--root DIR] [--report PATH] [--allow-ratio PCT]

Prints one PASS/FAIL line per check, exits non-zero when any check fails, and
writes the identical report (with a timestamp) to the report path.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None

# --------------------------------------------------------------------------- #
# configuration
# --------------------------------------------------------------------------- #

DEFAULT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT = os.path.join("brand_check", "VERIFY_REPORT.md")

CHROMA_MAX = 14          # max(r,g,b) - min(r,g,b) above this == chromatic
MIN_LOGO_WIDTH_PX = 120  # guideline: minimum web logo width
MAX_RATIO_DRIFT = 0.02   # 2 % tolerance on the asset aspect ratio
ARABIC_FLAG = "const ARABIC_ENABLED = false;"
PATTERN_FILES = ["assets/curve-pattern.svg", "assets/curve-pattern-dark.svg"]

HEX_RE = re.compile(
    r"(?<![\w#&])(#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3}))(?![\w-])"
)
RGB_RE = re.compile(r"\brgba?\(\s*([^)]*)\)", re.I)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I | re.S)
ATTR_RE = re.compile(
    r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""", re.I
)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I | re.S)
ASSET_REF_RE = re.compile(r"""(?:src|href)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
CSS_RULE_RE = re.compile(r"([^{}]*)\{([^{}]*)\}", re.S)
FONT_STACK_RE = re.compile(
    r"(?:font-family\s*:|--font[\w-]*\s*:)([^;}]*)", re.I
)


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def comment_ranges(text: str, kind: str):
    pat = CSS_COMMENT_RE if kind == "css" else HTML_COMMENT_RE
    return [(m.start(), m.end()) for m in pat.finditer(text)]


def in_ranges(offset: int, ranges) -> bool:
    return any(s <= offset < e for s, e in ranges)


def hex_chroma(tok: str):
    """-> (chroma, (r,g,b)) for '#abc' / '#abcd' / '#aabbcc' / '#aabbccdd'."""
    h = tok[1:]
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return max(r, g, b) - min(r, g, b), (r, g, b)


def rgb_chroma(args: str):
    """-> (chroma, (r,g,b)) for the inside of rgb()/rgba(); None if unparsable."""
    body = args.split("/")[0]
    raw = [p for p in re.split(r"[,\s]+", body.strip()) if p]
    vals = []
    for p in raw[:3]:
        pct = p.endswith("%")
        try:
            v = float(p.rstrip("%"))
        except ValueError:
            return None
        if pct:
            v = v / 100.0 * 255.0
        vals.append(int(round(v)))
    if len(vals) != 3:
        return None
    return max(vals) - min(vals), tuple(vals)


def scan_colours(path: str, kind: str):
    """-> (failures, comment_hits, neutrals, skipped_fragments)."""
    if not os.path.isfile(path):
        return None
    text = read_text(path)
    cranges = comment_ranges(text, kind)
    failures, comments, neutrals, skipped = [], [], [], 0

    def record(start, token, chroma, rgbv):
        nonlocal skipped
        if start > 0 and text[start - 1] in "\"'(":
            skipped += 1          # href="#hero" / url(#clip) style reference
            return
        entry = (line_of(text, start), token, chroma, rgbv)
        if in_ranges(start, cranges):
            comments.append(entry)
        elif chroma > CHROMA_MAX:
            failures.append(entry)
        else:
            neutrals.append(entry)

    for m in HEX_RE.finditer(text):
        ch, rgbv = hex_chroma(m.group(1))
        record(m.start(1), m.group(1), ch, rgbv)
    for m in RGB_RE.finditer(text):
        parsed = rgb_chroma(m.group(1))
        if parsed:
            record(m.start(), m.group(0).strip(), parsed[0], parsed[1])
    return failures, comments, neutrals, skipped


def css_declarations(css: str, class_name: str):
    """All declarations of rules whose selector mentions .class_name."""
    sel_re = re.compile(r"\." + re.escape(class_name) + r"(?![\w-])")
    out = []
    for m in CSS_RULE_RE.finditer(css):
        if not sel_re.search(m.group(1)):
            continue
        line = line_of(css, m.start(2))
        for decl in m.group(2).split(";"):
            if ":" not in decl:
                continue
            prop, val = decl.split(":", 1)
            out.append((prop.strip().lower(), val.strip(), line))
    return out


def px_value(value: str):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)px", value.strip(), re.I)
    return float(m.group(1)) if m else None


def parse_img_attrs(tag: str) -> dict:
    attrs = {}
    for m in ATTR_RE.finditer(tag):
        name = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        attrs.setdefault(name, (val if val is not None else "").strip())
    return attrs


def png_size(path: str):
    if Image is None or not os.path.isfile(path):
        return None
    try:
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# checks
# --------------------------------------------------------------------------- #

class Report:
    def __init__(self):
        self.lines = []
        self.failed = 0
        self.checks = 0

    def head(self, title: str, ok: bool, summary: str = ""):
        self.checks += 1
        if not ok:
            self.failed += 1
        tail = (" " + summary) if summary else ""
        self.lines.append("[%d] %s .......... %s%s"
                          % (self.checks, title, "PASS" if ok else "FAIL", tail))
        return ok

    def detail(self, text: str = ""):
        self.lines.append("    " + text if text else "")


def check_colour(rep: Report, styles_path: str, index_path: str):
    all_fail, all_notes = [], []
    ok = True
    for path, kind in ((styles_path, "css"), (index_path, "html")):
        res = scan_colours(path, kind)
        if res is None:
            ok = False
            all_fail.append((os.path.basename(path), 0, "file missing", 0))
            continue
        failures, comments, neutrals, skipped = res
        if failures:
            ok = False
        for line, token, chroma, rgbv in failures:
            all_fail.append((os.path.basename(path), line, token, chroma))
        for line, token, chroma, rgbv in comments:
            tag = token if chroma <= CHROMA_MAX else token + "  chroma=%d" % chroma
            all_notes.append("%s:%d  %s  [in comment]" % (os.path.basename(path), line, tag))
        all_notes.append("%s: %d colour literal(s) checked, %d neutral, "
                         "%d in comment, %d URL-fragment reference(s) skipped"
                         % (os.path.basename(path), len(failures) + len(comments) + len(neutrals),
                            len(neutrals), len(comments), skipped))

    rep.head("1. Colour: no chromatic colour", ok,
             "" if ok else "(%d offender(s))" % len(all_fail))
    for name, line, token, chroma in all_fail:
        rep.detail("OFFENDER  %s:%d  %s  (chroma %d > %d)" % (name, line, token, chroma, CHROMA_MAX))
    for note in all_notes:
        rep.detail(note)
    return ok


def check_typography(rep: Report, styles_path: str):
    if not os.path.isfile(styles_path):
        rep.head("2. Typography: Poppins + RB font stacks", False, "(styles.css missing)")
        return False
    css = read_text(styles_path)
    stacks = [m.group(1) for m in FONT_STACK_RE.finditer(css)]
    latin = [s for s in stacks if re.search(r"['\"]Poppins['\"]", s)]
    arabic = [s for s in stacks if re.search(r"['\"]RB['\"]", s)]
    ok = bool(latin) and bool(arabic)
    rep.head("2. Typography: Poppins + RB font stacks", ok)
    rep.detail("font stacks found: %d  ·  stacks naming 'Poppins': %d  ·  stacks naming 'RB': %d"
               % (len(stacks), len(latin), len(arabic)))
    for s in latin[:3]:
        rep.detail("Poppins -> %s" % " ".join(s.split())[:120])
    for s in arabic[:3]:
        rep.detail("RB      -> %s" % " ".join(s.split())[:120])
    if not latin:
        rep.detail("MISSING: no font-family / --font-* stack declares 'Poppins'")
    if not arabic:
        rep.detail("MISSING: no font-family / --font-* stack declares 'RB'")
    return ok


def check_arabic_toggle(rep: Report, script_path: str):
    if not os.path.isfile(script_path):
        rep.head("3. Arabic toggle stays hidden", False, "(script.js missing)")
        return False
    js = read_text(script_path)
    ok = ARABIC_FLAG in js
    rep.head("3. Arabic toggle stays hidden", ok)
    if ok:
        line = line_of(js, js.index(ARABIC_FLAG))
        rep.detail("script.js:%d  %s" % (line, ARABIC_FLAG))
    else:
        rep.detail("MISSING exact statement: %s" % ARABIC_FLAG)
        for m in re.finditer(r".*ARABIC_ENABLED.*", js):
            rep.detail("found instead  script.js:%d  %s"
                       % (line_of(js, m.start()), m.group(0).strip()[:120]))
    return ok


def check_logo(rep: Report, index_path: str, styles_path: str, root: str):
    if not os.path.isfile(index_path):
        rep.head("4. Logo usage: width >= 120px, aspect intact", False, "(index.html missing)")
        return False
    html = read_text(index_path)
    css = read_text(styles_path) if os.path.isfile(styles_path) else ""

    logo_tags = []
    for m in IMG_RE.finditer(html):
        attrs = parse_img_attrs(m.group(0))
        if "logo" in attrs.get("class", "").lower():
            logo_tags.append((line_of(html, m.start()), attrs))

    ok = True
    findings = []
    for line, attrs in logo_tags:
        src = attrs.get("src", "")
        classes = attrs.get("class", "").split()
        asset = os.path.join(root, src.replace("/", os.sep))
        size = png_size(asset)
        real_ar = (size[0] / size[1]) if size else None

        html_w = px_value(attrs.get("width", ""))
        html_h = px_value(attrs.get("height", ""))

        # cascade-aware: later declarations of the same property win
        decls = []
        for cls in classes:
            decls.extend((cls,) + d for d in css_declarations(css, cls))
        effective = {}
        for cls, prop, val, cline in decls:
            effective.setdefault(prop, []).append((val, cline, cls))

        css_w = css_minw = css_h = None
        css_notes = []
        for prop, occurrences in effective.items():
            val, cline, cls = occurrences[-1]          # last one wins
            if prop == "width" and px_value(val) is not None:
                css_w = px_value(val)
                css_notes.append("styles.css:%d  .%s { width: %s }" % (cline, cls, val))
            elif prop == "min-width" and px_value(val) is not None:
                css_minw = px_value(val)
                css_notes.append("styles.css:%d  .%s { min-width: %s }" % (cline, cls, val))
            elif prop == "height" and px_value(val) is not None:
                css_h = px_value(val)
                css_notes.append("styles.css:%d  .%s { height: %s }" % (cline, cls, val))
            elif prop == "height":
                css_notes.append("styles.css:%d  .%s { height: %s }  (fluid, not hard-coded px)"
                                 % (cline, cls, val))
            elif prop in ("width", "height") and val.strip().lower() == "auto":
                css_notes.append("styles.css:%d  .%s { %s: auto }  (aspect preserved)"
                                 % (cline, cls, prop))
            elif prop == "width":
                css_notes.append("styles.css:%d  .%s { width: %s }" % (cline, cls, val))
            for val_i, line_i, cls_i in occurrences[:-1]:
                css_notes.append("  (note) .%s { %s: %s } at styles.css:%d is overridden by "
                                 "%s at styles.css:%d"
                                 % (cls_i, prop, val_i, line_i, val, cline))
        declared_w = max([v for v in (html_w, css_w, css_minw) if v is not None], default=None)
        findings.append("HTML:%d  <img src=\"%s\" class=\"%s\">" % (line, src, attrs.get("class", "")))
        findings.append("   declared width ...... %s px   (guideline minimum %d px)"
                        % ("%.0f" % declared_w if declared_w else "none", MIN_LOGO_WIDTH_PX))
        if css_notes:
            findings.extend("   " + n for n in css_notes)
        if real_ar:
            findings.append("   asset aspect ratio ... %.3f  (%s: %dx%d)"
                            % (real_ar, src, size[0], size[1]))
        else:
            findings.append("   asset aspect ratio ... UNREADABLE (%s)" % src)

        if declared_w is None or declared_w < MIN_LOGO_WIDTH_PX:
            ok = False
            findings.append("   FAIL: declared width below %d px" % MIN_LOGO_WIDTH_PX)

        # --- hard-coded width/height pair vs the real asset ratio -----------
        pairs = []
        if html_w and html_h:
            pairs.append(("HTML width/height attributes", html_w, html_h, line))
        if css_w and css_h:
            pairs.append(("CSS width/height", css_w, css_h, 0))
        for label, w, h, _ln in pairs:
            pair_ar = w / h
            if not real_ar:
                continue
            drift = abs(pair_ar - real_ar) / real_ar
            if drift > MAX_RATIO_DRIFT:
                ok = False
                findings.append("   FAIL: %s = %.0fx%.0f -> ratio %.3f vs asset %.3f "
                                "(%.1f%% off, tolerance %.0f%%)"
                                % (label, w, h, pair_ar, real_ar, drift * 100,
                                   MAX_RATIO_DRIFT * 100))
            else:
                findings.append("   ok: %s = %.0fx%.0f -> ratio %.3f (drift %.1f%%)"
                                % (label, w, h, pair_ar, drift * 100))

    # --- favicon -------------------------------------------------------------
    favicon = None
    for m in LINK_RE.finditer(html):
        attrs = parse_img_attrs(m.group(0))
        rel = attrs.get("rel", "").lower()
        if "icon" in rel:
            favicon = (attrs.get("rel", ""), attrs.get("href", ""))
            break
    if favicon:
        rel, href = favicon
        is_mark = bool(re.match(r"^assets/curve-mark[\w.-]*\.png$", href))
        if not is_mark:
            ok = False
        findings.append("favicon (rel=\"%s\") ... %s  -> %s"
                        % (rel, href or "(empty)",
                           "icon mark (correct)" if is_mark
                           else "NOT an assets/curve-mark-*.png — wordmark/full logo not allowed"))
    else:
        ok = False
        findings.append("favicon ................ no <link rel=\"icon\"> found")

    rep.head("4. Logo usage: width >= 120px, aspect intact", ok,
             "(%d logo <img> tag(s))" % len(logo_tags))
    for f in findings:
        rep.detail(f)
    return ok


def check_assets(rep: Report, index_path: str, root: str):
    if not os.path.isfile(index_path):
        rep.head("5. Assets referenced by index.html exist", False, "(index.html missing)")
        return False
    html = read_text(index_path)
    refs = []
    for m in ASSET_REF_RE.finditer(html):
        val = m.group(1) if m.group(1) is not None else m.group(2)
        if val and val.startswith("assets/"):
            refs.append((line_of(html, m.start()), val))
    missing = [(ln, r) for ln, r in refs
               if not os.path.exists(os.path.join(root, r.replace("/", os.sep)))]
    ok = not missing
    rep.head("5. Assets referenced by index.html exist", ok,
             "%d referenced, %d missing" % (len(refs), len(missing)))
    for ln, r in missing:
        rep.detail("MISSING  index.html:%d  %s" % (ln, r))
    dupes = sorted({r for _l, r in refs})
    rep.detail("unique asset paths: %d" % len(dupes))
    return ok


def check_pattern(rep: Report, styles_path: str, root: str):
    missing_files = [f for f in PATTERN_FILES
                     if not os.path.exists(os.path.join(root, f.replace("/", os.sep)))]
    unref = []
    if os.path.isfile(styles_path):
        css = read_text(styles_path)
        for f in PATTERN_FILES:
            base = os.path.basename(f)
            if not re.search(r"url\(\s*[\"']?[^)\"']*" + re.escape(base), css):
                unref.append(f)
    else:
        unref = list(PATTERN_FILES)
    ok = not missing_files and not unref
    rep.head("6. Brand pattern files exist and are referenced from styles.css", ok)
    for f in PATTERN_FILES:
        status = "on disk" if f not in missing_files else "MISSING ON DISK"
        rep.detail("%-34s %s%s" % (f, status,
                                   "" if f not in unref else "  ·  not referenced in styles.css"))
    if os.path.isfile(styles_path):
        css = read_text(styles_path)
        for m in re.finditer(r"url\(\s*[\"']?[^)\"']*curve-pattern[\w.-]*", css):
            rep.detail("referenced at styles.css:%d" % line_of(css, m.start()))
    return ok


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main(argv=None) -> int:
    global MAX_RATIO_DRIFT

    ap = argparse.ArgumentParser(description="CURVE brand-compliance verifier")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="site root (default: script directory)")
    ap.add_argument("--report", default=DEFAULT_REPORT, help="report path, relative to --root")
    ap.add_argument("--allow-ratio", type=float, default=MAX_RATIO_DRIFT,
                    help="aspect-ratio tolerance as a fraction (default 0.02)")
    args = ap.parse_args(argv)

    MAX_RATIO_DRIFT = args.allow_ratio

    root = os.path.abspath(args.root)
    index_path = os.path.join(root, "index.html")
    styles_path = os.path.join(root, "styles.css")
    script_path = os.path.join(root, "script.js")
    stamp = _dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    rep = Report()
    header = [
        "CURVE - brand compliance verification",
        "site root : %s" % root,
        "timestamp : %s" % stamp,
        "files     : " + "  ".join(
            "%s (%d bytes)" % (n, os.path.getsize(os.path.join(root, n)))
            if os.path.isfile(os.path.join(root, n)) else "%s (MISSING)" % n
            for n in ("index.html", "styles.css", "script.js")),
        "rules     : chroma <= %d  ·  min logo width %dpx  ·  aspect drift <= %.0f%%"
        % (CHROMA_MAX, MIN_LOGO_WIDTH_PX, MAX_RATIO_DRIFT * 100),
        "",
    ]

    check_colour(rep, styles_path, index_path)
    rep.lines.append("")
    check_typography(rep, styles_path)
    rep.lines.append("")
    check_arabic_toggle(rep, script_path)
    rep.lines.append("")
    check_logo(rep, index_path, styles_path, root)
    rep.lines.append("")
    check_assets(rep, index_path, root)
    rep.lines.append("")
    check_pattern(rep, styles_path, root)

    rep.lines.append("")
    verdict = ("RESULT: PASS - %d/%d checks passed" % (rep.checks, rep.checks)
               if rep.failed == 0 else
               "RESULT: FAIL - %d of %d checks failed" % (rep.failed, rep.checks))
    rep.lines.append(verdict)
    rep.lines.append("exit code: %d" % (1 if rep.failed else 0))

    body = "\n".join(header + rep.lines) + "\n"
    print(body, end="")

    report_path = args.report if os.path.isabs(args.report) else os.path.join(root, args.report)
    try:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write("# CURVE - brand compliance verification\n\n```\n" + body + "```\n")
        print("report written: %s" % report_path)
    except OSError as exc:
        print("could not write report %s: %s" % (report_path, exc), file=sys.stderr)

    return 1 if rep.failed else 0


if __name__ == "__main__":
    sys.exit(main())
