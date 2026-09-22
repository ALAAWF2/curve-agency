"""Put Alaa's IN MOTION artwork in the hero instead of the typed headline.

1. measure the ink box of paner/panner-0١.svg in the browser and write a tight-cropped
   vector copy (assets/svg/hero-in-motion.svg) whose background matches the page ground
2. swap the h1 text for the artwork (text stays for screen readers)
3. compact the mobile hero so the empty space above the pill is gone
"""
import asyncio, base64, json, re, time, urllib.request
from pathlib import Path
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "assets" / "svg"
SRC = "paner/panner-0\u0661.svg"

JS = """
async (url) => {
  const img = await new Promise(res => { const i = new Image(); i.onload=()=>res(i); i.onerror=()=>res(null); i.src = url; });
  if (!img) return JSON.stringify({error: 'load failed'});
  const W = 960, H = 540;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const x = c.getContext('2d'); x.drawImage(img, 0, 0, W, H);
  const d = x.getImageData(0, 0, W, H).data;
  let x0 = W, y0 = H, x1 = -1, y1 = -1;
  for (let y = 0; y < H; y++) for (let px = 0; px < W; px++) {
    const a = d[(y*W+px)*4+3];
    if (a > 12) { if (px<x0) x0=px; if (px>x1) x1=px; if (y<y0) y0=y; if (y>y1) y1=y; }
  }
  // لون البكسل عند الزاوية (خلفية العمل الفني)
  const px = (xx, yy) => { const i = (yy*W+xx)*4; return [d[i], d[i+1], d[i+2], d[i+3]]; };
  // وأغمق بكسل (الحبر)
  let darkest = [255,255,255], dmin = 999;
  for (let y = y0; y <= y1; y += 3) for (let pp = x0; pp <= x1; pp += 3) {
    const i = (y*W+pp)*4; const v = (d[i]+d[i+1]+d[i+2])/3;
    if (v < dmin) { dmin = v; darkest = [d[i], d[i+1], d[i+2]]; }
  }
  return JSON.stringify({x0, y0, x1, y1, W, H, corner: px(2,2), darkest});
}
"""


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=120 * 1024 * 1024) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Page.enable", "params": {}}))
        await ws.send(json.dumps({"id": 2, "method": "Runtime.enable", "params": {}}))
        n = 3
        async def send(m, p=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": m, "params": p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == n:
                    return r.get("result", {})
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/_svg_sheet.html"})
        await asyncio.sleep(3)
        res = await send("Runtime.evaluate", {"expression":
            f"({JS})('/{SRC}'.replace(' ', '%20'))", "awaitPromise": True, "returnByValue": True})
        m = json.loads(res["result"]["value"])
    print("قياس العمل الفني:", m)
    if "error" in m:
        raise SystemExit(1)

    src = (R / SRC).read_text(encoding="utf-8", errors="ignore")
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
    sx, sy = vb[2] / m["W"], vb[3] / m["H"]
    bx, by = vb[0] + m["x0"] * sx, vb[1] + m["y0"] * sy
    bw, bh = (m["x1"] - m["x0"] + 1) * sx, (m["y1"] - m["y0"] + 1) * sy
    body = re.sub(r"<\?xml[^>]*\?>", "", src)
    body = re.sub(r'viewBox="[^"]+"', f'viewBox="{bx:.2f} {by:.2f} {bw:.2f} {bh:.2f}"', body, count=1)
    body = re.sub(r'\swidth="[^"]*"', "", body, count=1)
    body = re.sub(r'\sheight="[^"]*"', "", body, count=1)
    (OUT / "hero-in-motion.svg").write_text(body, encoding="utf-8")
    print(f"✓ assets/svg/hero-in-motion.svg  viewBox {bx:.1f} {by:.1f} {bw:.1f} {bh:.1f} · نسبة {bw/bh:.2f}")


asyncio.run(main())
