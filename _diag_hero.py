
import asyncio, json, time, urllib.request, websockets
async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=120*1024*1024) as ws:
        n=0
        async def send(m,p=None):
            nonlocal n; n+=1
            await ws.send(json.dumps({"id":n,"method":m,"params":p or {}}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==n: return r.get("result",{})
        await send("Page.enable"); await send("Runtime.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride", {"width":390,"height":844,"deviceScaleFactor":2,"mobile":True})
        await send("Page.navigate", {"url":"http://127.0.0.1:8080/?v=%d"%int(time.time())})
        await asyncio.sleep(5)
        js = """(() => {
          const out = [];
          document.querySelectorAll('.hero-section *').forEach(e => {
            const r = e.getBoundingClientRect();
            if (r.height > 900) out.push([e.tagName + '.' + (e.className||'').toString().slice(0,40), Math.round(r.height), Math.round(r.width)]);
          });
          const img = document.querySelector('.hero-art');
          const cs = img ? getComputedStyle(img) : null;
          return JSON.stringify({big: out.slice(0,10),
            img: img ? {nat: [img.naturalWidth, img.naturalHeight], w: img.width, h: img.height,
                        cssW: cs.width, cssH: cs.height, complete: img.complete} : null,
            heroH: Math.round(document.querySelector('.hero-section').getBoundingClientRect().height)});
        })()"""
        r = await send("Runtime.evaluate", {"expression": js, "returnByValue": True})
        print(r["result"]["value"])
asyncio.run(main())
