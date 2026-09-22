"""Audit every section's heading vs body colour, and read the work-grid structure."""
import asyncio, json, time, urllib.request
import websockets

JS = """
(() => {
  const out = [];
  const secs = document.querySelectorAll('section, footer, header');
  const isHeading = el => /^(H1|H2|H3|H4)$/.test(el.tagName);
  secs.forEach(s => {
    const rows = [];
    s.querySelectorAll('h1,h2,h3,h4,.section-headline,.card-statement,.work-title,.service-title,.step-title,.why-card-title,.banner-title,.form-title,.contact-giant-title,.section-idx,.section-desc,.work-desc,.service-body,.step-desc,.why-card-body,.hero-lead,.contact-lead,.card-caption,.banner-desc,.about-body-text,.why-lead-text,.source-text,.work-client')
      .forEach(el => {
        const cs = getComputedStyle(el);
        rows.push([el.tagName.toLowerCase() + '.' + (el.className || '').split(' ')[0],
                   el.textContent.trim().slice(0, 26), cs.color, cs.fontSize, cs.fontWeight]);
      });
    out.push([s.id || s.className.split(' ').pop(), rows.slice(0, 14)]);
  });
  const grid = document.querySelector('#work-grid');
  return JSON.stringify({sections: out,
    workCards: grid ? grid.children.length : null,
    gridStyle: grid ? getComputedStyle(grid).gridTemplateColumns + ' | gap ' + getComputedStyle(grid).gap : null,
    workCardHTML: grid && grid.firstElementChild ? grid.firstElementChild.outerHTML.slice(0, 700) : null});
})()
"""


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=90 * 1024 * 1024) as ws:
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
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/?v=%d" % int(time.time())})
        await asyncio.sleep(4.5)
        r = await send("Runtime.evaluate", {"expression": JS, "returnByValue": True})
        d = json.loads(r["result"]["value"])

    print(f"شبكة الأعمال: {d['workCards']} كرت · {d['gridStyle']}")
    print("\n=== ألوان العناوين مقابل النصوص لكل قسم ===")
    for name, rows in d["sections"]:
        if not rows:
            continue
        print(f"\n[{name}]")
        for tag, txt, col, fs, fw in rows:
            kind = "عنوان" if tag.startswith(("h1", "h2", "h3", "h4")) else "نص  "
            print(f"   {kind} {tag:<34} {col:<22} {fs:>7} w{fw:<4} {txt}")
    print("\n=== HTML كرت عمل (نموذج) ===")
    print(d["workCardHTML"])

asyncio.run(main())
