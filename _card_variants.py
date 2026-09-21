"""Render the featured-card variants so Alaa can pick one (no file changes yet)."""
import asyncio, base64, json, urllib.request, time, os, websockets

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_check")
os.makedirs(OUT, exist_ok=True)
URL = "http://127.0.0.1:8080/?v=%d" % int(time.time())

VARIANTS = {
    # A — current: fully inverted white card
    "A_white_now": "",
    # B — subtle: no white slab, just a slightly lifted surface + brighter hairline
    "B_subtle": """
      .service-card.featured-service, .service-card.featured-service:hover {
        background: rgba(255,255,255,0.085) !important;
        border-color: rgba(255,255,255,0.42) !important;
      }
      .service-card.featured-service .service-title,
      .service-card.featured-service .service-num { color: #fff !important; }
      .service-card.featured-service .service-sub { color: rgba(255,255,255,0.72) !important; }
      .service-card.featured-service .service-body { color: rgba(255,255,255,0.62) !important; }
      .service-card.featured-service .service-items { border-top-color: rgba(255,255,255,0.14) !important; }
      .service-card.featured-service .service-items li { color: rgba(255,255,255,0.5) !important; }
      .service-card.featured-service .service-items li::before { color: #fff !important; }
      .service-card.featured-service .service-tag-badge,
      .service-card.featured-service .service-tag-badge.highlight {
        background: rgba(255,255,255,0.14) !important; color:#fff !important; border-color: rgba(255,255,255,0.3) !important;
      }""",
    # C — no emphasis at all: all six cards identical
    "C_none": """
      .service-card.featured-service, .service-card.featured-service:hover {
        background: var(--bg-card) !important; border-color: var(--border-dim) !important;
      }
      .service-card.featured-service .service-title,
      .service-card.featured-service .service-num { color: var(--text-pure) !important; }
      .service-card.featured-service .service-num { color: var(--text-dim) !important; }
      .service-card.featured-service .service-sub { color: var(--accent) !important; }
      .service-card.featured-service .service-body { color: var(--text-muted) !important; }
      .service-card.featured-service .service-items { border-top-color: var(--border-dim) !important; }
      .service-card.featured-service .service-items li { color: var(--text-dim) !important; }
      .service-card.featured-service .service-items li::before { color: var(--accent) !important; }
      .service-card.featured-service .service-tag-badge.highlight {
        background: rgba(255,255,255,0.05) !important; color: var(--text-muted) !important; border-color: transparent !important;
      }""",
    # D — white card made obviously intentional: brand pattern ghosted inside it
    "D_white_pattern": """
      .service-card.featured-service { position: relative; overflow: hidden; }
      .service-card.featured-service::after {
        content: ""; position: absolute; inset: -35%; z-index: 0; pointer-events: none;
        background-image: url('assets/curve-pattern-dark.svg'); background-size: 96px 96px;
        opacity: 0.085; transform: rotate(45deg);
      }
      .service-card.featured-service > * { position: relative; z-index: 1; }""",
}


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

        await send("Page.enable")
        await send("Runtime.enable")
        await send("Network.enable")
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 1000, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": URL})
        await asyncio.sleep(5)
        await send("Runtime.evaluate", {"expression":
                   "(()=>{const s=document.createElement('style');s.id='x';s.textContent='.reveal{opacity:1!important;transform:none!important}';document.head.appendChild(s);document.querySelectorAll('.reveal').forEach(e=>e.classList.add('active'));for(let y=0;y<document.body.scrollHeight;y+=600)scrollTo(0,y);scrollTo(0,0);return 1})()"})
        await asyncio.sleep(2.5)

        for name, css in VARIANTS.items():
            await send("Runtime.evaluate", {"expression":
                       "(()=>{let x=document.getElementById('variant'); if(!x){x=document.createElement('style');x.id='variant';document.head.appendChild(x);} x.textContent=%s; return 1})()"
                       % json.dumps(css)})
            await asyncio.sleep(0.7)
            r = await send("Runtime.evaluate", {"expression":
                           "(()=>{const el=document.getElementById('services');const b=el.getBoundingClientRect();return JSON.stringify({y:Math.max(0,b.top+scrollY),h:Math.min(b.height,1500)})})()",
                           "returnByValue": True})
            c = json.loads(r["result"]["value"])
            res = await send("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                                       "clip": {"x": 0, "y": c["y"], "width": 1440, "height": c["h"], "scale": 1}})
            p = os.path.join(OUT, f"card_{name}.png")
            open(p, "wb").write(base64.b64decode(res["data"]))
            print("  ✓", os.path.relpath(p).replace("\\", "/"))


asyncio.run(main())
