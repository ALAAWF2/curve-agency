"""Capture the hero at mobile and desktop widths after the artwork swap."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "brand_check"


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
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        for name, w, h, scale in (("mobile", 390, 844, 2), ("desktop", 1440, 900, 1)):
            await send("Emulation.setDeviceMetricsOverride",
                       {"width": w, "height": h, "deviceScaleFactor": scale, "mobile": w < 700})
            await send("Page.navigate", {"url": "http://127.0.0.1:8080/?v=%d" % int(time.time())})
            await asyncio.sleep(5)
            info = await send("Runtime.evaluate", {"expression": """
              (() => {
                document.querySelectorAll('.reveal').forEach(e => { e.style.opacity='1'; e.style.transform='none'; });
                const art = document.querySelector('.hero-art');
                const hero = document.querySelector('.hero-section');
                const r = art.getBoundingClientRect(), hr = hero.getBoundingClientRect();
                const pill = document.querySelector('.hero-tag-wrap').getBoundingClientRect();
                return JSON.stringify({artW: Math.round(r.width), artH: Math.round(r.height),
                  artTop: Math.round(r.top), heroH: Math.round(hr.height),
                  gapPillToArt: Math.round(r.top - pill.bottom),
                  vh: innerHeight, scrollH: document.body.scrollHeight});
              })()
            """, "returnByValue": True})
            await asyncio.sleep(1.2)
            shot = await send("Page.captureScreenshot", {"format": "png"})
            p = OUT / f"hero_{name}.png"
            p.write_bytes(base64.b64decode(shot["data"]))
            print(f"✓ {p.name}  {info['result']['value']}")


asyncio.run(main())
