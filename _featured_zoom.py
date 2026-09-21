"""Zoom on the featured card to judge how visible the ghosted pattern really is."""
import asyncio, base64, json, urllib.request, time, os, websockets
from PIL import Image, ImageStat

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "brand_check")
URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=80 * 1024 * 1024) as ws:
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
        await send("Network.enable"); await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 1000, "deviceScaleFactor": 2, "mobile": False})
        await send("Page.navigate", {"url": URL})
        await asyncio.sleep(5)
        await send("Runtime.evaluate", {"expression":
                   "(()=>{const s=document.createElement('style');s.textContent='.reveal{opacity:1!important;transform:none!important}';document.head.appendChild(s);document.querySelectorAll('.reveal').forEach(e=>e.classList.add('active'));for(let y=0;y<document.body.scrollHeight;y+=600)scrollTo(0,y);scrollTo(0,0);return 1})()"})
        await asyncio.sleep(2.5)
        r = await send("Runtime.evaluate", {"expression":
                       "(()=>{const el=document.querySelector('.service-card.featured-service');const b=el.getBoundingClientRect();const cs=getComputedStyle(el,'::after');return JSON.stringify({x:b.x,y:b.y+scrollY,w:b.width,h:b.height,op:cs.opacity,bg:cs.backgroundImage.slice(0,60),size:cs.backgroundSize})})()",
                       "returnByValue": True})
        info = json.loads(r["result"]["value"])
        print("  featured card:", json.dumps(info, ensure_ascii=False))
        res = await send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                                   "clip": {"x": info["x"], "y": info["y"], "width": info["w"],
                                                            "height": info["h"], "scale": 2}})
        p = os.path.join(OUT, "featured_zoom.png")
        open(p, "wb").write(base64.b64decode(res["data"]))
        print("  saved", os.path.relpath(p).replace("\\", "/"))

        im = Image.open(p).convert("L")
        st = ImageStat.Stat(im)
        print(f"  متوسط السطوع={st.mean[0]:.1f}  الانحراف={st.stddev[0]:.2f}  (الانحراف العالي = النمط ظاهر)")
        # measure a clean area away from text (top-left corner block)
        w, h = im.size
        patch = im.crop((int(w * 0.62), int(h * 0.02), int(w * 0.97), int(h * 0.18)))
        ps = ImageStat.Stat(patch)
        print(f"  منطقة فاضية: متوسط={ps.mean[0]:.1f} انحراف={ps.stddev[0]:.2f} مدى={patch.getextrema()}")


asyncio.run(main())
