"""Diagnose why work thumbnails look empty and whether the pattern band renders."""
import asyncio, json, urllib.request, sys

CDP = 9223
JS = r"""
(() => {
  const out = {};
  const p = document.querySelector('.brand-pattern');
  if (p) { const r = p.getBoundingClientRect(); const cs = getComputedStyle(p);
    out.pattern = {w: Math.round(r.width), h: Math.round(r.height), opacity: cs.opacity,
                   bg: cs.backgroundImage.slice(0, 60), transform: cs.transform.slice(0, 30)}; }
  const b = document.querySelector('.brand-band');
  if (b) { const r = b.getBoundingClientRect(); const cs = getComputedStyle(b);
    out.band = {h: Math.round(r.height), w: Math.round(r.width), y: Math.round(r.top + window.scrollY),
                opacity: cs.opacity, bg: cs.backgroundImage.slice(0, 60), size: cs.backgroundSize}; }
  else out.band = 'NOT IN DOM';

  const imgs = [...document.querySelectorAll('#work img')];
  out.workImgs = imgs.slice(0, 6).map(i => {
    const cs = getComputedStyle(i);
    let lum = null;
    try {
      const c = document.createElement('canvas'); c.width = 24; c.height = 16;
      const x = c.getContext('2d'); x.drawImage(i, 0, 0, 24, 16);
      const d = x.getImageData(0, 0, 24, 16).data;
      let s = 0; for (let k = 0; k < d.length; k += 4) s += (d[k] + d[k+1] + d[k+2]) / 3;
      lum = Math.round(s / (d.length / 4));
    } catch (e) { lum = 'ERR ' + e.name; }
    return {src: (i.currentSrc || i.src).split('/').pop(), complete: i.complete,
            nw: i.naturalWidth, nh: i.naturalHeight, opacity: cs.opacity,
            filter: cs.filter, mix: cs.mixBlendMode, meanLuminance: lum,
            parentOverlay: (() => { const par = i.parentElement;
              return par ? [...par.children].map(c => c.className || c.tagName).join(',') : ''; })()};
  });
  const wc = document.querySelector('#work .work-media, #work figure, #work .work-thumb');
  if (wc) { const cs = getComputedStyle(wc);
    out.workMedia = {cls: wc.className, bg: cs.backgroundColor, overlay: [...wc.children].map(c => c.className).join(',')}; }
  return JSON.stringify(out, null, 1);
})()
"""


async def main():
    import websockets
    tabs = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP}/json/list").read())
    t = next(x for x in tabs if "127.0.0.1:8080" in (x.get("url") or ""))
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=40 * 1024 * 1024) as ws:
        n = 0

        async def send(m, p=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": m, "params": p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == n:
                    return r.get("result", {})

        await send("Runtime.enable")
        # make sure everything is loaded
        await send("Runtime.evaluate", {"expression":
                   "for (let y=0;y<document.body.scrollHeight;y+=500) scrollTo(0,y); scrollTo(0,0); 1"})
        await asyncio.sleep(2.5)
        r = await send("Runtime.evaluate", {"expression": JS, "returnByValue": True})
        print(r["result"]["value"])


asyncio.run(main())
