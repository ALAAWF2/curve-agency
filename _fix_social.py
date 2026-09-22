"""Send Alaa the IN MOTION artwork itself + harden the social preview (absolute URLs, JPG)."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
from PIL import Image
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
WEB = R / "assets" / "web"
BC = R / "brand_check"
BANNER = "paner/panner-0\u0661.svg"


async def shoot(url_path, w, h, out):
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
                   {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/" + url_path})
        await asyncio.sleep(2.6)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        out.write_bytes(base64.b64decode(shot["data"]))
        print(f"✓ {out.name} {out.stat().st_size} بايت")


async def main():
    # 1) البانر بحجمه الكامل 1920×1080
    await shoot(BANNER, 1920, 1080, BC / "in_motion_1920x1080.png")
    # 2) صورة السوشال عبر إطار يملأ الخلفية (بلا شرائط)
    await shoot("_og_frame.html", 1200, 630, WEB / "og-image.png")


asyncio.run(main())

# نسخة JPG أخف وأوسع توافقاً للمعاينات
png = Image.open(WEB / "og-image.png").convert("RGB")
png.save(WEB / "og-image.jpg", quality=88, optimize=True, progressive=True)
print(f"✓ og-image.jpg {(WEB / 'og-image.jpg').stat().st_size} بايت")

# 3) اعتمد JPG في الوسوم المطلقة
H = R / "index.html"
h = H.read_text(encoding="utf-8")
base = "https://alaawf2.github.io/curve-agency/"
h = h.replace(f'content="{base}assets/web/og-image.png"', f'content="{base}assets/web/og-image.jpg"')
h = h.replace('<meta property="og:image:type" content="image/png">',
              '<meta property="og:image:type" content="image/jpeg">')
H.write_text(h, encoding="utf-8")
print("✓ og:image ->", "og-image.jpg" if "og-image.jpg" in h else "لم يتغير")
