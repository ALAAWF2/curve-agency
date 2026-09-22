"""Build the two grey themes as a variable+override layer, render both, and measure contrast.

Theme A: page ground = #727272 (the guideline's 55% tint of black — the values Alaa gave)
Theme B: page ground = #EDEDED with #727272 as the secondary text (what the page-23 website
         mockup in the new guideline actually measures: ground #EDEDED 86% of pixels,
         #727272 = 0.58% -> it is the grey TYPE, not the ground)
"""
import asyncio, base64, json, time, urllib.request
import websockets

URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())
OUT = r"C:/Users/Orange/workspace/curve-site/brand_check"

HEAD = """
:root{
  --paper:%(paper)s; --text-pure:%(ink)s; --text-primary:%(ink)s;
  --text-muted:%(sec)s; --text-dim:%(sec)s; --accent:%(ink)s;
  --bg-surface:rgba(0,0,0,.03); --bg-card:rgba(0,0,0,.04); --bg-card-hover:rgba(0,0,0,.07);
  --border-dim:rgba(0,0,0,.12); --border-light:rgba(0,0,0,.22); --border-hover:rgba(0,0,0,.5);
}
html,body,.site-wrapper{background-color:%(paper)s !important;color:%(ink)s !important;}
.hero,.section,.capabilities,.services,.about,.process,.stats,.work,.why-curve,.partners,
.brand-band,.site-footer{background-color:%(paper)s !important;}
h1,h2,h3,h4,.hero-title,.section-headline,.card-statement,.service-title,.step-title,
.why-card-title,.work-title,.banner-title,.form-title,.stat-num,.title-solid{color:%(ink)s !important;}
.hero-lead,.section-desc,.work-desc,.service-body,.step-desc,.why-card-body,.about-body-text,
.why-lead-text,.contact-lead,.card-caption,.banner-desc,.source-text,.work-badge,.work-client,
.section-idx,.detail-label,.social-label,.service-num,.step-num,.stat-label{color:%(sec)s !important;}
.service-card,.why-card,.work-card,.process-step,.stat-cell,.partner-cell,.form-container{
  background-color:%(card)s !important;border-color:rgba(0,0,0,.12) !important;}
.partner-cell img,.brand-logo img{filter:invert(1) grayscale(1) contrast(1.05) !important;}
.work-visual img{filter:grayscale(1) contrast(1.04) !important;}
.brand-band,[class*="pattern"]{background-image:url('assets/curve-pattern-dark.svg') !important;
  opacity:.06 !important;}
.title-outline{-webkit-text-stroke-color:rgba(0,0,0,.45) !important;color:transparent !important;}
"""

THEMES = {
    "A_ground727272": dict(paper="#727272", ink="#000000", sec="#EDEDED", card="rgba(255,255,255,.06)"),
    "B_groundEDEDED": dict(paper="#EDEDED", ink="#000000", sec="#727272", card="rgba(255,255,255,.65)"),
}


def lum(hexc):
    h = hexc.lstrip("#")
    rgb = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

CASES = list(THEMES.items())


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=80 * 1024 * 1024) as ws:
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
                   {"width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False})

        for name, tok in CASES:
            css = HEAD % tok
            await send("Page.navigate", {"url": URL}); await asyncio.sleep(4.5)
            script = f"""
            (() => {{
              document.querySelectorAll('style#theme').forEach(e => e.remove());
              const s = document.createElement('style'); s.id='theme'; s.textContent = {json.dumps(css)};
              document.head.appendChild(s);
              document.querySelectorAll('.reveal').forEach(e => {{
                e.style.opacity='1'; e.style.transform='none'; e.classList.add('visible'); }});
              return 'ok';
            }})()
            """
            await send("Runtime.evaluate", {"expression": script, "returnByValue": True})
            await asyncio.sleep(2)
            for sec, sel in (("about", "#about"), ("work", "#work")):
                await send("Runtime.evaluate", {"expression":
                           f"(() => {{ const e=document.querySelector('{sel}'); if(e) window.scrollTo(0, e.getBoundingClientRect().top+scrollY); return 1; }})()",
                           "returnByValue": True})
                await asyncio.sleep(1.6)
                shot = await send("Page.captureScreenshot", {"format": "png"})
                path = f"{OUT}/theme_{name}_{sec}.png"
                open(path, "wb").write(base64.b64decode(shot["data"]))
                print(f"  ✓ {path}")
            print(f"  تباين {name}: نص أساسي {ratio(tok['ink'], tok['paper']):.2f}:1 · نص ثانوي {ratio(tok['sec'], tok['paper']):.2f}:1")


asyncio.run(main())
