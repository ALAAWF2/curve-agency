"""Measure the ink bounding box of Alaa's logo SVGs (in the browser), then emit black,
tight-cropped SVG assets for the light theme: header/footer wordmark, mark, favicon."""
import asyncio, json, re, time, urllib.request
from pathlib import Path
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "assets" / "svg"
OUT.mkdir(exist_ok=True)

CAND = {
    "logo07": "logo/logo-0\u0667.svg",
    "logo08": "logo/logo-0\u0668.svg",
    "el01":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0661.svg",
    "el02":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0662.svg",
    "el03":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0663.svg",
    "el05":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0665.svg",
    "el06":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0666.svg",
    "el04":   "PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0664.svg",
    "strip1": "paner/panner-0\u0661-0\u0662.svg",
    "strip2": "paner/panner-0\u0662.svg",
    "hero_banner": "paner/panner-0\u0661.svg",
}

JS = """
async (list) => {
  const out = [];
  for (const [key, url] of list) {
    const r = await new Promise(res => { const i = new Image(); i.onload = () => res(i); i.onerror = () => res(null); i.src = url + '?t=' + Date.now(); });
    if (!r) { out.push([key, null]); continue; }
    const W = 900, H = 900;
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const x = c.getContext('2d'); x.drawImage(r, 0, 0, W, H);
    const d = x.getImageData(0, 0, W, H).data;
    let x0 = W, y0 = H, x1 = -1, y1 = -1;
    for (let y = 0; y < H; y++) for (let px = 0; px < W; px++) {
      const a = d[(y * W + px) * 4 + 3];
      if (a > 24) { if (px < x0) x0 = px; if (px > x1) x1 = px; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    out.push([key, {w: W, h: H, x0, y0, x1, y1, natW: r.naturalWidth, natH: r.naturalHeight,
                    inkW: x1 - x0 + 1, inkH: y1 - y0 + 1, ratio: +((x1 - x0 + 1) / (y1 - y0 + 1)).toFixed(3)}]);
  }
  return JSON.stringify(out);
}
"""


async def main():
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
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/_svg_sheet.html"})
        await asyncio.sleep(3.5)
        # نستخدم مسارات مطلقة بالنسبة للموقع
        lst = [[k, "/" + v.replace(" ", "%20").replace("&", "%26")] for k, v in CAND.items()]
        res = await send("Runtime.evaluate", {"expression": f"({JS})({json.dumps(lst)})",
                                             "awaitPromise": True, "returnByValue": True})
        data = json.loads(res["result"]["value"])

    print(f"{'مفتاح':<12}{'الملف':<44}{'نسبة الحبر':>10}  {'صندوق الحبر (من 900)':>22}")
    info = {}
    for key, m in data:
        info[key] = m
        if m:
            print(f"{key:<12}{CAND[key][:42]:<44}{m['ratio']:>10}  {m['x0']},{m['y0']} → {m['x1']},{m['y1']}")
        else:
            print(f"{key:<12}{CAND[key][:42]:<44}{'فشل التحميل':>10}")

    # ---------- نولّد نسخ سودا مقصوصة ----------
    def emit(src_rel, key, out_name, pad_frac=0.0):
        m = info.get(key)
        if not m:
            return None
        src = (R / src_rel).read_text(encoding="utf-8", errors="ignore")
        vb = re.search(r'viewBox="([^"]+)"', src)
        if not vb:
            return None
        vx, vy, vw, vh = [float(x) for x in vb.group(1).split()]
        # نسبة صندوق الحبر من الصورة 900×900 إلى إحداثيات الـviewBox
        sx, sy = vw / m["w"], vh / m["h"]
        bx = vx + m["x0"] * sx
        by = vy + m["y0"] * sy
        bw = m["inkW"] * sx
        bh = m["inkH"] * sy
        pad = pad_frac * max(bw, bh)
        bx -= pad; by -= pad; bw += 2 * pad; bh += 2 * pad
        body = src
        body = re.sub(r"<\?xml[^>]*\?>", "", body)
        body = re.sub(r"<defs>.*?</defs>", "", body, flags=re.S)
        body = re.sub(r'class="b"', 'fill="#000000"', body)
        body = body.replace("#efefef", "#000000")
        body = re.sub(r'id="a"', f'id="{out_name.replace(".svg","")}"', body)
        body = re.sub(r'viewBox="[^"]+"', f'viewBox="{bx:.2f} {by:.2f} {bw:.2f} {bh:.2f}"', body, count=1)
        (OUT / out_name).write_text(body, encoding="utf-8")
        return f"assets/svg/{out_name}  ({len(body)} حرف · viewBox {bx:.1f} {by:.1f} {bw:.1f} {bh:.1f})"

    print("\n=== ملفات سودا مولّدة ===")
    for rel, key, name in [("logo/logo-0\u0667.svg", "logo07", "curve-logo-black.svg"),
                           ("logo/logo-0\u0668.svg", "logo08", "curve-mark-black.svg"),
                           ("PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0661.svg", "el01", "element-arch.svg"),
                           ("PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0663.svg", "el03", "element-pinwheel.svg"),
                           ("PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0665.svg", "el05", "element-rotor.svg"),
                           ("PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0666.svg", "el06", "element-corner.svg"),
                           ("PATTERN & ELEMENTS/PATTERN & ELEMENTS-0\u0662.svg", "el02", "element-hook.svg")]:
        r = emit(rel, key, name)
        print("  ✓", r if r else f"تخطّي {name}")

asyncio.run(main())
