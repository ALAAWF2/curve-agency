"""Rasterise Alaa's IN MOTION artwork with a TRANSPARENT ground so it can sit in the hero
over the existing photograph instead of the typed headline (the artwork ships with a flat
#efefef background and two embedded rasters, so a luminance->alpha key reproduces it)."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
SRC = "paner/panner-0\u0661.svg"
W, H = 2880, 1620
RAW = R / "brand_check" / "_hero_art_raw.png"
OUT = R / "assets" / "web" / "hero-in-motion.png"

JS = """
async ([url, w, h]) => {
  const img = await new Promise(r => { const i = new Image(); i.onload=()=>r(i); i.src = url; });
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const x = c.getContext('2d');
  x.imageSmoothingQuality = 'high';
  x.drawImage(img, 0, 0, w, h);
  return c.toDataURL('image/png');
}
"""


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=400 * 1024 * 1024) as ws:
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
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/_svg_sheet.html"})
        await asyncio.sleep(3)
        res = await send("Runtime.evaluate", {"expression":
            f"({JS})(['/{SRC}'.replace(' ', '%20'), {W}, {H}])", "awaitPromise": True, "returnByValue": True})
        data = res["result"]["value"].split(",", 1)[1]
    RAW.write_bytes(base64.b64decode(data))
    print(f"✓ رسم خام {RAW.name} ({RAW.stat().st_size} بايت)")


asyncio.run(main())

# ---- مفتاح الإضاءة → شفافية: الأسود يبقى، الأرضية تصير شفافة ----
im = Image.open(RAW).convert("RGB")
a = np.asarray(im).astype(np.float32)
lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)   # 0 = أسود · 239 = الأرضية
# خفّض الأرضية (#efefef) لشفافية 0 مع إبقاء التدرّجات الناعمة مرئية
alpha = np.clip((239.0 - lum) * (255.0 / 239.0), 0, 255)
rgba = np.dstack([np.zeros_like(lum, dtype=np.uint8), np.zeros_like(lum, dtype=np.uint8),
                  np.zeros_like(lum, dtype=np.uint8), alpha.astype(np.uint8)])
Image.fromarray(rgba, "RGBA").save(OUT, optimize=True)
print(f"✓ {OUT.name} ({OUT.stat().st_size} بايت · {im.size[0]}×{im.size[1]} · شفافية {100*(alpha<8).mean():.1f}% من البكسلات)")
