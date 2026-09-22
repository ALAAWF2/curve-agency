
import asyncio, base64, json, time, urllib.request, websockets
from PIL import Image
import numpy as np
async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=200*1024*1024) as ws:
        n=0
        async def send(m,p=None):
            nonlocal n; n+=1
            await ws.send(json.dumps({"id":n,"method":m,"params":p or {}}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==n: return r.get("result",{})
        await send("Page.enable"); await send("Runtime.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride", {"width":1200,"height":630,"deviceScaleFactor":1,"mobile":False})
        await send("Page.navigate", {"url":"http://127.0.0.1:8080/_og_frame.html?v=%d"%int(time.time())})
        await asyncio.sleep(3)
        s=await send("Page.captureScreenshot", {"format":"png"})
        open(r"C:/Users/Orange/workspace/curve-site/assets/web/og-image.png","wb").write(base64.b64decode(s["data"]))
        print("OK rendered")
asyncio.run(main())
a = np.asarray(Image.open(r"C:/Users/Orange/workspace/curve-site/assets/web/og-image.png").convert("RGB"))
print("مقاس:", a.shape)
print("أعمدة يسار:", a[:, 0:3].reshape(-1,3).mean(axis=0).round(0), "· يمين:", a[:, -3:].reshape(-1,3).mean(axis=0).round(0))
print("هل في شرائط بيضاء (255)؟", bool((a[:, 0:6] > 250).all()) or bool((a[:, -6:] > 250).all()))
