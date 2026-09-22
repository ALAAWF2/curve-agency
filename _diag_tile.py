
import asyncio, base64, json, time, urllib.request, websockets
async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=90*1024*1024) as ws:
        n=0
        async def send(m,p=None):
            nonlocal n; n+=1
            await ws.send(json.dumps({"id":n,"method":m,"params":p or {}}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==n: return r.get("result",{})
        await send("Page.enable"); await send("Runtime.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride", {"width":1440,"height":900,"deviceScaleFactor":1,"mobile":False})
        # 1) معاينة البلاطة
        await send("Page.navigate", {"url":"http://127.0.0.1:8080/_tile_preview.html?v=%d"%int(time.time())})
        await asyncio.sleep(2.5)
        s=await send("Page.captureScreenshot", {"format":"png"})
        open(r"C:/Users/Orange/workspace/curve-site/brand_check/diag_tile.png","wb").write(base64.b64decode(s["data"]))
        # 2) الشريط داخل الموقع
        await send("Page.navigate", {"url":"http://127.0.0.1:8080/?v=%d"%int(time.time())})
        await asyncio.sleep(4.5)
        js="""(() => { const b=document.querySelector('.brand-band'); const r=b.getBoundingClientRect();
             return JSON.stringify({x:0,y:Math.round(r.top+scrollY-110),w:1440,h:Math.round(r.height+220)}); })()"""
        box=json.loads((await send("Runtime.evaluate", {"expression":js,"returnByValue":True}))["result"]["value"])
        s=await send("Page.captureScreenshot", {"format":"png","captureBeyondViewport":True,
             "clip":{"x":box["x"],"y":box["y"],"width":box["w"],"height":box["h"],"scale":1}})
        open(r"C:/Users/Orange/workspace/curve-site/brand_check/diag_band4.png","wb").write(base64.b64decode(s["data"]))
        print("OK")
asyncio.run(main())
