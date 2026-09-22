"""Diagnose the brand band + hero element rendering, and screenshot them closely."""
import asyncio, base64, json, time, urllib.request
import websockets

OUT = r"C:/Users/Orange/workspace/curve-site/brand_check"
JS = """
(() => {
  const band = document.querySelector('.brand-band');
  const hero = document.querySelector('.hero');
  const after = hero ? getComputedStyle(hero, '::after') : null;
  const b = band ? getComputedStyle(band) : null;
  const r = band ? band.getBoundingClientRect() : null;
  return JSON.stringify({
    band: b ? {h: r.height, y: Math.round(r.top + scrollY), img: b.backgroundImage,
               size: b.backgroundSize, repeat: b.backgroundRepeat, pos: b.backgroundPosition,
               color: b.backgroundColor, opacity: b.opacity} : null,
    heroAfter: after ? {w: after.width, h: after.height, img: after.backgroundImage.slice(0,90),
                        opacity: after.opacity, z: after.zIndex, display: after.display} : null
  });
})()
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
        await send("Page.enable"); await send("Runtime.enable"); await send("Network.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/?v=%d" % int(time.time())})
        await asyncio.sleep(4.5)
        r = await send("Runtime.evaluate", {"expression": JS, "returnByValue": True})
        print(r["result"]["value"])

        # مقاس تحميل صورة النمط
        net = await send("Runtime.evaluate", {"expression":
            "(async () => { const r = await fetch('assets/svg/pattern-official.svg'); return r.status + ' ' + r.headers.get('content-type'); })()",
            "awaitPromise": True, "returnByValue": True})
        print("pattern fetch:", net["result"]["value"])

        # صورة مقرّبة لشريط العلامة
        box = json.loads(r["result"]["value"])["band"]
        if box:
            await send("Runtime.evaluate", {"expression":
                "(() => { const e=document.querySelector('.brand-band'); window.scrollTo(0, e.getBoundingClientRect().top+scrollY-200); return 1; })()",
                "returnByValue": True})
            await asyncio.sleep(1.2)
            shot = await send("Page.captureScreenshot", {"format": "png"})
            open(f"{OUT}/diag_band.png", "wb").write(base64.b64decode(shot["data"]))
            print("✓ diag_band.png")

        # لوحة النمط الرسمي وحدها
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/_pattern_preview.html?v=%d" % int(time.time())})
        await asyncio.sleep(2.5)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        open(f"{OUT}/diag_pattern.png", "wb").write(base64.b64decode(shot["data"]))
        print("✓ diag_pattern.png")

asyncio.run(main())
