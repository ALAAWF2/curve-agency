"""Capture CURVE site screenshots through the debug Chrome on CDP 9223.

Usage: python _capture.py <out_prefix> [--mobile] [--sections hero,about,services]
Opens (or reuses) a tab at 127.0.0.1:8080, forces a fresh load, then captures
full-page and per-section PNGs. Never touches other tabs (SIFR / قوم!).
"""
import asyncio, base64, json, os, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
CDP = 9223
URL = "http://127.0.0.1:8080/"


def tab():
    for t in json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP}/json/list").read()):
        if t.get("type") == "page" and "127.0.0.1:8080" in (t.get("url") or ""):
            return t
    # create one if missing
    return json.loads(urllib.request.urlopen(f"http://127.0.0.1:{CDP}/json/new?{URL}").read())


async def main():
    import websockets
    args = sys.argv[1:]
    prefix = args[0] if args else "shot"
    mobile = "--mobile" in args
    W, H = (390, 844) if mobile else (1440, 900)

    t = tab()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_check")
    os.makedirs(out_dir, exist_ok=True)

    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=80 * 1024 * 1024) as ws:
        n = 0

        async def send(method, params=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": method, "params": params or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get("id") == n:
                    if "error" in r:
                        raise RuntimeError(f"{method}: {r['error']}")
                    return r.get("result", {})

        await send("Page.enable")
        await send("Runtime.enable")
        await send("Network.enable")
        try:
            await send("Page.bringToFront")
        except Exception:
            pass
        await send("Network.setCacheDisabled", {"cacheDisabled": True})
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": mobile})
        import time as _t
        await send("Page.navigate", {"url": f"{URL}?v={int(_t.time())}"})
        await asyncio.sleep(4.5)
        # force scroll-reveal elements visible, else sections capture blank
        await send("Runtime.evaluate", {"expression": """
            (() => {
              const s = document.createElement('style');
              s.textContent = '.reveal{opacity:1!important;transform:none!important}';
              document.head.appendChild(s);
              document.querySelectorAll('.reveal').forEach(e => e.classList.add('active'));
              // step-scroll so lazy images below the fold actually load
              const H = document.body.scrollHeight;
              for (let y = 0; y < H; y += 600) window.scrollTo(0, y);
              window.scrollTo(0, 0);
              // background tabs postpone lazy images; force them
              document.querySelectorAll('img[loading="lazy"]').forEach(i => {
                i.loading = 'eager';
                const s = i.src; i.src = ''; i.src = s;
              });
              return document.querySelectorAll('.reveal').length;
            })()""", "returnByValue": True})
        await asyncio.sleep(3.5)

        async def shot(name, clip=None, full=False):
            p = {"format": "png", "captureBeyondViewport": full}
            if clip:
                p["clip"] = {**clip, "scale": 1}
            res = await send("Page.captureScreenshot", p)
            path = os.path.join(out_dir, f"{prefix}_{name}.png")
            with open(path, "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("  ✓", os.path.relpath(path).replace("\\", "/"))

        # full page
        m = await send("Page.getLayoutMetrics")
        css = m.get("cssContentSize") or m.get("contentSize")
        full_h = int(min(css["height"], 30000))
        print(f"  ارتفاع الصفحة الكامل: {full_h}px · عرض {int(css['width'])}px")
        await shot("full", clip={"x": 0, "y": 0, "width": W, "height": full_h})

        # key sections by id
        ids = ["hero", "about", "services", "process", "why-curve", "stats",
               "work", "partners", "contact"]
        for sec in ids:
            r = await send("Runtime.evaluate", {
                "expression": f"""(() => {{
                    const el = document.getElementById('{sec}');
                    if (!el) return null;
                    const b = el.getBoundingClientRect();
                    return JSON.stringify({{x:0, y: Math.max(0, b.top + window.scrollY),
                        width: {W}, height: Math.min(b.height, 2400)}});
                }})()""", "returnByValue": True})
            val = r.get("result", {}).get("value")
            if not val:
                print(f"  – قسم {sec}: غير موجود")
                continue
            c = json.loads(val)
            await shot(sec, clip=c, full=True)

    print("تم.")


asyncio.run(main())
