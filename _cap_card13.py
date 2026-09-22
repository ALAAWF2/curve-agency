
import asyncio, base64, json, time, urllib.request, websockets
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
        await send("Emulation.setDeviceMetricsOverride", {"width":1440,"height":1000,"deviceScaleFactor":1,"mobile":False})
        await send("Page.navigate", {"url":"http://127.0.0.1:8080/?v=%d"%int(time.time())})
        await asyncio.sleep(5)
        js = """(() => { const c=document.querySelector('.work-card[data-index="13"]');
              c.scrollIntoView({block:'center'}); document.querySelectorAll('.reveal').forEach(e=>{e.style.opacity='1';e.style.transform='none';});
              const r=c.getBoundingClientRect();
              return JSON.stringify({y:Math.round(r.top+scrollY-60), w:Math.round(r.width), h:Math.round(r.height), cols:getComputedStyle(c).gridColumn}); })()"""
        d = json.loads((await send("Runtime.evaluate", {"expression":js,"returnByValue":True}))["result"]["value"])
        print("كرت 13:", d)
        await asyncio.sleep(1.5)
        s=await send("Page.captureScreenshot", {"format":"png","captureBeyondViewport":True,
             "clip":{"x":0,"y":d["y"],"width":1440,"height":900,"scale":1}})
        open(r"C:/Users/Orange/workspace/curve-site/brand_check/hdr_card13.png","wb").write(base64.b64decode(s["data"]))
        print("OK")
asyncio.run(main())
