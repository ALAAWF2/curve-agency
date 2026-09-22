"""Publish Alaa's 'IN MOTION' banner (paner/panner-0١.svg) as the site's social preview:
rasterise it to 1200x630 PNG and wire the Open Graph / Twitter meta tags."""
import asyncio, base64, json, re, time, urllib.request
from pathlib import Path
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "assets" / "web"
OUT.mkdir(parents=True, exist_ok=True)
PNG = OUT / "og-image.png"


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
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1200, "height": 630, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/paner/panner-0\u0661.svg"})
        await asyncio.sleep(2.5)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        PNG.write_bytes(base64.b64decode(shot["data"]))
        print(f"✓ {PNG}  ({PNG.stat().st_size} بايت)")


asyncio.run(main())

# ---- وسوم السوشال في index.html ----
H = R / "index.html"
h = H.read_text(encoding="utf-8")
meta = ('  <meta property="og:type" content="website">\n'
        '  <meta property="og:title" content="CURVE — Creative Agency | Jeddah">\n'
        '  <meta property="og:description" content="Full-service creative agency: brand identity, digital design, content creation and media production. Ignite the motion.">\n'
        '  <meta property="og:image" content="assets/web/og-image.png">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <meta name="twitter:image" content="assets/web/og-image.png">\n')
if "og:image" not in h:
    h = h.replace('<link rel="icon" type="image/svg+xml"', meta + '  <link rel="icon" type="image/svg+xml"')
    H.write_text(h, encoding="utf-8")
    print("✓ og/twitter meta added")
else:
    print("· og meta already present")
print("  og:image count:", h.count("og-image.png"))
