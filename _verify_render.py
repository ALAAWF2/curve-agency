"""End-to-end check of the SIFR-alignment pass: measure the RENDERED page via CDP."""
import asyncio, json, os, sys, time, urllib.request
import websockets

URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())

JS = r"""
(() => {
  const px = el => el ? getComputedStyle(el).fontSize : null;
  const lh = el => el ? getComputedStyle(el).lineHeight : null;
  const out = {
    vw: innerWidth,
    navDesktop: [...document.querySelectorAll('.nav-link')].map(a => a.textContent.trim()),
    navMobile: [...document.querySelectorAll('.mobile-nav-link')].map(a => a.textContent.trim()),
    heroFont: px(document.querySelector('.hero-title')),
    heroLineHeight: lh(document.querySelector('.hero-title')),
    sectionHeadline: px(document.querySelector('.section-headline')),
    sectionHeadlineLH: lh(document.querySelector('.section-headline')),
    sectionIdx: [...document.querySelectorAll('.section-idx')].slice(0,3).map(e => e.textContent.trim()),
    containerPad: getComputedStyle(document.documentElement).getPropertyValue('--container-pad').trim(),
    sectionPadY: getComputedStyle(document.documentElement).getPropertyValue('--section-pad-y').trim(),
    filterHasBorder: (() => { const f = document.querySelector('.filter-btn');
      if (!f) return 'no filter'; const c = getComputedStyle(f);
      return `border=${c.borderTopWidth} radius=${c.borderRadius} bg=${c.backgroundColor}`; })(),
    workVisual: (() => { const w = document.querySelector('.work-visual');
      if (!w) return 'n/a'; const c = getComputedStyle(w);
      return `radius=${c.borderTopLeftRadius} border=${c.borderTopWidth} ratio=${c.aspectRatio}`; })(),
    badgePosition: (() => { const b = document.querySelector('.work-badge');
      return b ? getComputedStyle(b).position + ' | parent=' + b.parentElement.className : 'n/a'; })(),
    stagger: (() => { const cards = [...document.querySelectorAll('.work-grid > .work-card')];
      return cards.slice(0,2).map(c => Math.round(c.getBoundingClientRect().top + scrollY)); })(),
    contactGround: (() => { const s = document.querySelector('#contact');
      return s ? getComputedStyle(s).backgroundColor : 'n/a'; })(),
    contactTitleColor: (() => { const t = document.querySelector('#contact .title-solid');
      return t ? getComputedStyle(t).color : 'n/a'; })(),
    chroma: (() => {
      // scan every element's computed colour-ish properties for a hue
      const bad = [];
      const huey = v => {
        const m = v.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return false;
        const [r,g,b] = [+m[1], +m[2], +m[3]];
        return Math.max(r,g,b) - Math.min(r,g,b) > 14;
      };
      for (const el of document.querySelectorAll('*')) {
        const c = getComputedStyle(el);
        for (const p of ['color','backgroundColor','borderTopColor','webkitTextStrokeColor']) {
          if (huey(c[p])) bad.push(el.className + ' / ' + p + ' = ' + c[p]);
        }
        if (bad.length > 6) break;
      }
      return bad.length ? bad : 'ZERO (achromatic)';
    })(),
  };
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

        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True})
        await asyncio.sleep(2.5)
        r = await send("Runtime.evaluate", {"expression":
                       "JSON.stringify({mobileNav:[...document.querySelectorAll('.mobile-nav-link')].map(a=>a.textContent.trim()), heroFont:getComputedStyle(document.querySelector('.hero-title')).fontSize, docWidth:document.documentElement.scrollWidth, overflow: document.documentElement.scrollWidth > innerWidth + 2})",
                       "returnByValue": True})
        print(r["result"]["value"])


asyncio.run(main())
