
import asyncio, base64, json, urllib.request, time, websockets
URL='http://127.0.0.1:8080/_font_test.html?v=%d'%int(time.time())
async def main():
    tabs=json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json/list').read())
    t=[x for x in tabs if x.get('type')=='page'][0]
    async with websockets.connect(t['webSocketDebuggerUrl'],max_size=60*1024*1024) as ws:
        n=0
        async def send(m,p=None):
            nonlocal n
            n+=1
            await ws.send(json.dumps({'id':n,'method':m,'params':p or {}}))
            while True:
                r=json.loads(await ws.recv())
                if r.get('id')==n: return r.get('result',{})
        await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable')
        await send('Network.setCacheDisabled',{'cacheDisabled':True})
        await send('Emulation.setDeviceMetricsOverride',{'width':1280,'height':1000,'deviceScaleFactor':1,'mobile':False})
        await send('Page.navigate',{'url':URL}); await asyncio.sleep(4)
        m=await send('Page.getLayoutMetrics'); h=int((m.get('cssContentSize') or m.get('contentSize'))['height'])
        res=await send('Page.captureScreenshot',{'format':'png','captureBeyondViewport':True,'clip':{'x':0,'y':0,'width':1280,'height':min(h,1400),'scale':1}})
        open('brand_check/rb_specimen.png','wb').write(base64.b64decode(res['data']))
        print('saved rb_specimen.png', 1280, min(h,1400))
asyncio.run(main())
