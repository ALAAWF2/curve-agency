"""Render Alaa's banner SVGs to PNG, then check whether the screenshot he just sent is one of them."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "brand_check"
TARGETS = {
    "panner01":    "paner/panner-0\u0661.svg",
    "panner01_01": "paner/panner-0\u0661-0\u0661.svg",
    "panner01_03": "paner/panner-0\u0661-0\u0663.svg",
    "page1":       "assets/page1.svg",
}
JS = """
async (list) => {
  const out = [];
  for (const [key, url, w, h] of list) {
    const img = await new Promise(res => { const i = new Image(); i.onload=()=>res(i); i.onerror=()=>res(null); i.src = url; });
    if (!img) { out.push([key, null]); continue; }
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const x = c.getContext('2d');
    x.fillStyle = '#EDEDED'; x.fillRect(0, 0, w, h);
    x.drawImage(img, 0, 0, w, h);
    out.push([key, c.toDataURL('image/png')]);
  }
  return JSON.stringify(out.map(([k, d]) => [k, d ? d.length : 0]));
}
"""


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=200 * 1024 * 1024) as ws:
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
        await asyncio.sleep(3)
        lst = [[k, "/" + v.replace(" ", "%20"), 1600, 900] for k, v in TARGETS.items()]
        res = await send("Runtime.evaluate", {"expression": f"({JS})({json.dumps(lst)})",
                                              "awaitPromise": True, "returnByValue": True})
        print("sizes:", res["result"]["value"])

        # نعيد النداء لكل ملف منفرداً لنجلب البيانات
        for k, v in TARGETS.items():
            one = [[k, "/" + v.replace(" ", "%20"), 1600, 900]]
            res = await send("Runtime.evaluate", {"expression":
                f"""(async () => {{ const o = await ({JS})({json.dumps(one)}); const raw = JSON.parse(o);
                     const img = new Image(); await new Promise(r => {{ img.onload = r; img.src = document.createElement('canvas').toDataURL(); }});
                     return o; }})()""", "awaitPromise": True, "returnByValue": True})
        # طريقة أبسط: نستخدم Page.navigate على الملف ونلتقط
        for k, v in TARGETS.items():
            await send("Emulation.setDeviceMetricsOverride",
                       {"width": 1600, "height": 900, "deviceScaleFactor": 1, "mobile": False})
            await send("Page.navigate", {"url": "http://127.0.0.1:8080/" + v.replace(" ", "%20")})
            await asyncio.sleep(2.2)
            shot = await send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True})
            p = OUT / f"asset_{k}.png"
            p.write_bytes(base64.b64decode(shot["data"]))
            print("✓", p.name)


asyncio.run(main())

# --- هل صورة علاء = أحد هذه الملفات؟ ---
his = Image.open(r"C:/Users/Orange/AppData/Local/hermes/cache/images/img_99cc5eb8152d.jpg").convert("L").resize((64, 36))
hv = np.asarray(his, dtype=float)
print("\n=== مقارنة صورته مع المرشّحين (فرق متوسط أصغر = أشبه) ===")
cands = [("asset_panner01.png", OUT / "asset_panner01.png"),
         ("asset_panner01_01.png", OUT / "asset_panner01_01.png"),
         ("asset_panner01_03.png", OUT / "asset_panner01_03.png"),
         ("موقعنا الآن (final_hero.png)", R / "brand_check" / "final_hero.png")]
for name, p in cands:
    if not p.exists():
        continue
    im = np.asarray(Image.open(p).convert("L").resize((64, 36)), dtype=float)
    print(f"  {name:<32} فرق {np.abs(im - hv).mean():6.2f}")
