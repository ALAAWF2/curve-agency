"""Inventory every SVG Alaa added, then render one contact sheet so I can see them all."""
import base64, html, json, os, re, time, urllib.request
from pathlib import Path
import asyncio, websockets

ROOT = Path(r"C:/Users/Orange/workspace/curve-site")
SKIP = {".git", "node_modules", "_g2", "brand_check", "site_screenshots", "reference_screenshots", "_guideline_pages"}

svgs = []
for p in sorted(ROOT.rglob("*.svg")):
    if any(part in SKIP for part in p.parts):
        continue
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    vb = re.search(r'viewBox="([^"]+)"', txt)
    fills = sorted(set(re.findall(r"fill:\s*(#[0-9a-fA-F]{3,6})", txt) + re.findall(r'fill="(#[0-9a-fA-F]{3,6})"', txt)))
    svgs.append(dict(rel=str(p.relative_to(ROOT)).replace("\\", "/"), size=p.stat().st_size,
                     vb=vb.group(1) if vb else "?", fills=fills[:4]))

print(f"=== {len(svgs)} ملف SVG ===")
for s in svgs:
    print(f"  {s['size']:>8} B  {s['rel']:<42} viewBox={s['vb']:<18} fills={s['fills']}")

# ---- contact sheet on the approved light ground ----
cells = "\n".join(
    f'<div class="cell"><div class="box"><img src="{s["rel"]}"></div>'
    f'<div class="cap">{s["rel"]}<br><span>{s["size"]}B · {s["vb"]}</span></div></div>'
    for s in svgs)
sheet = f"""<!doctype html><meta charset="utf-8"><style>
body{{background:#EDEDED;font-family:Consolas,monospace;margin:0;padding:18px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
.cell{{background:#fff;border:1px solid rgba(0,0,0,.15)}}
.box{{height:150px;display:flex;align-items:center;justify-content:center;padding:10px;background:#EDEDED}}
.box img{{max-width:100%;max-height:130px;object-fit:contain}}
.cap{{font-size:10px;padding:5px 7px;color:#000;border-top:1px solid rgba(0,0,0,.12);word-break:break-all}}
.cap span{{color:#727272}}</style>
<div class="grid">{cells}</div>"""
(ROOT / "_svg_sheet.html").write_text(sheet, encoding="utf-8")
print("\n✓ _svg_sheet.html كتبت")


async def shot():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=90 * 1024 * 1024) as ws:
        n = 0
        async def send(m, p=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": m, "params": p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == n:
                    return r.get("result", {})
        await send("Page.enable"); await send("Runtime.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        h = 260 * ((len(svgs) + 3) // 4) + 60
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1400, "height": min(h, 2400), "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": f"http://127.0.0.1:8080/_svg_sheet.html?v={int(time.time())}"})
        await asyncio.sleep(5)
        r = await send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
        out = ROOT / "brand_check" / "svg_contact_sheet.png"
        out.write_bytes(base64.b64decode(r["data"]))
        print(f"✓ {out}")

asyncio.run(shot())
