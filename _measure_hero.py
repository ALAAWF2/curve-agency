
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
          const g = s => { const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect();
            return {top:Math.round(r.top), bottom:Math.round(r.bottom), h:Math.round(r.height)}; };
          const hero=g('.hero-section'), pill=g('.hero-tag-wrap'), art=g('.hero-art'),
                grid=g('.hero-bottom-grid'), lead=g('.hero-lead'), cta=g('.hero-cta-group'),
                head=g('.site-header');
          return JSON.stringify({vh:innerHeight, head, hero, pill, art, grid, lead, cta,
            gap_head_pill: pill.top-head.bottom, gap_pill_art: art.top-pill.bottom,
            gap_art_grid: grid.top-art.bottom, gap_grid_lead: lead.top-grid.top,
            gap_cta_heroend: hero.bottom-cta.bottom});
        })()"""
        r = await send("Runtime.evaluate", {"expression": js, "returnByValue": True})
        d = json.loads(r["result"]["value"])
        for k, v in d.items():
            print(f"  {k:18s} {v}")
asyncio.run(main())
