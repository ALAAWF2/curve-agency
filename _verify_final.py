"""Post-change check: measured type numbers + the Arabic toggle guard."""
import asyncio, json, time, urllib.request
import websockets

URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())

JS = r"""
(() => {
  const t = document.querySelector('.hero-title');
  const h = document.querySelector('.section-headline');
  const out = {
    viewport: innerWidth,
    heroFont: getComputedStyle(t).fontSize,
    heroLineHeight: getComputedStyle(t).lineHeight,
    heroLHratio: (parseFloat(getComputedStyle(t).lineHeight) / parseFloat(getComputedStyle(t).fontSize)).toFixed(3),
    heroFontVW: (parseFloat(getComputedStyle(t).fontSize) / innerWidth * 100).toFixed(2) + 'vw',
    sectionFont: getComputedStyle(h).fontSize,
    sectionLHratio: (parseFloat(getComputedStyle(h).lineHeight) / parseFloat(getComputedStyle(h).fontSize)).toFixed(3),
    containerPadPx: getComputedStyle(document.querySelector('.container')).paddingLeft,
    containerMarginPct: (parseFloat(getComputedStyle(document.querySelector('.container')).paddingLeft) / innerWidth * 100).toFixed(2) + 'vw',
    filterRule: (() => { const f = document.querySelector('.work-filters');
      return getComputedStyle(f).borderBottomWidth + ' ' + getComputedStyle(f).borderBottomColor; })(),
    staggerPx: (() => { const c = [...document.querySelectorAll('.work-grid > .work-card')];
      if (c.length < 2) return null;
      return Math.round((c[1].getBoundingClientRect().top + scrollY) - (c[0].getBoundingClientRect().top + scrollY)); })(),
    langBefore: document.documentElement.lang,
    storedBefore: localStorage.getItem('curve_lang'),
  };
  // try to force the (hidden) language toggle into Arabic
  const btn = document.getElementById('lang-toggle');
  localStorage.setItem('curve_lang', 'ar');
  if (btn) { btn.style.display = 'block'; btn.click(); btn.click(); }
  out.toggleExists = !!btn;
  out.langAfterForcedClicks = document.documentElement.lang;
  out.storedAfterForcedClicks = localStorage.getItem('curve_lang');
  out.toggleVisibleAfterClicks = btn ? getComputedStyle(btn).display : null;
  return JSON.stringify(out, null, 1);
})()
"""


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=60 * 1024 * 1024) as ws:
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
                   {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": URL})
        await asyncio.sleep(5)
        r = await send("Runtime.evaluate", {"expression": JS, "returnByValue": True})
        print(r["result"]["value"])


asyncio.run(main())
