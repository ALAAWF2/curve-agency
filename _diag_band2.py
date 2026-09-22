"""Center the brand band, screenshot it, and read the contact-form field colours."""
import asyncio, base64, json, time, urllib.request
import websockets

OUT = r"C:/Users/Orange/workspace/curve-site/brand_check"


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
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 620, "deviceScaleFactor": 1.4, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/?v=%d" % int(time.time())})
        await asyncio.sleep(4.5)
        # الشريط + خصائص حقول الفورم
        js = """
        (() => {
          const band = document.querySelector('.brand-band');
          if (band) { const y = band.getBoundingClientRect().top + scrollY; window.scrollTo(0, y - 268); }
          const inp = document.querySelector('.form-group input');
          const cs = inp ? getComputedStyle(inp) : null;
          const lbl = document.querySelector('.form-group label');
          const ph = cs ? getComputedStyle(inp, '::placeholder') : null;
          return JSON.stringify({
            bandY: band ? Math.round(band.getBoundingClientRect().top) : null,
            input: cs ? {color: cs.color, bg: cs.backgroundColor, border: cs.borderColor} : null,
            label: lbl ? getComputedStyle(lbl).color : null,
            placeholder: ph ? ph.color : null,
            afterImg: band ? getComputedStyle(band, '::after').backgroundImage.slice(0, 80) : null,
            afterOpacity: band ? getComputedStyle(band, '::after').opacity : null
          });
        })()
        """
        r = await send("Runtime.evaluate", {"expression": js, "returnByValue": True})
        print(r["result"]["value"])
        await asyncio.sleep(1.4)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        open(f"{OUT}/diag_band2.png", "wb").write(base64.b64decode(shot["data"]))
        print("✓ diag_band2.png")


asyncio.run(main())
