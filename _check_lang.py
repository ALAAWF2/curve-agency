
import asyncio, json, time, urllib.request, websockets
URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())
JS = "JSON.stringify({lang:document.documentElement.lang, stored:localStorage.getItem('curve_lang'), toggle:getComputedStyle(document.getElementById('lang-toggle')).display})"
async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=40*1024*1024) as ws:
        n = 0
        async def send(m, p=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": m, "params": p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == n: return r.get("result", {})
        await send("Page.enable"); await send("Runtime.enable")
        await send("Network.enable"); await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Page.navigate", {"url": URL}); await asyncio.sleep(5)
        r = await send("Runtime.evaluate", {"expression": JS, "returnByValue": True})
        print("after clean reload ->", r["result"]["value"])
asyncio.run(main())
