"""Read the header design out of Alaa's nav-strip SVGs and compare it with the live header."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
import numpy as np
from PIL import Image
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")
OUT = R / "brand_check"
STRIPS = {"strip_a": "paner/panner-0\u0661-0\u0662.svg", "strip_b": "paner/panner-0\u0662.svg"}


async def main():
    tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9223/json/list").read())
    t = next(x for x in tabs if x.get("type") == "page")
    async with websockets.connect(t["webSocketDebuggerUrl"], max_size=200 * 1024 * 1024) as ws:
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
        for k, v in STRIPS.items():
            await send("Emulation.setDeviceMetricsOverride",
                       {"width": 1920, "height": 112, "deviceScaleFactor": 1, "mobile": False})
            await send("Page.navigate", {"url": "http://127.0.0.1:8080/" + v.replace(" ", "%20")})
            await asyncio.sleep(2.2)
            shot = await send("Page.captureScreenshot", {"format": "png"})
            (OUT / f"{k}.png").write_bytes(base64.b64decode(shot["data"]))

        # مقاييس الهيدر الحيّ
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/?v=%d" % int(time.time())})
        await asyncio.sleep(4.5)
        js = """
        (() => {
          const hd = document.querySelector('.site-header');
          const inner = document.querySelector('.header-inner');
          const logo = document.querySelector('.logo-img');
          const cta = document.querySelector('.site-header .btn-outline, .site-header .btn');
          const nav = document.querySelector('.nav-links, .nav-menu, nav ul');
          const r = e => e ? e.getBoundingClientRect() : null;
          const R1 = r(inner), R2 = r(logo), R3 = r(cta);
          return JSON.stringify({vw: innerWidth,
            headerH: r(hd).height, headerPadPct: +(R1.left / innerWidth * 100).toFixed(2),
            logoW: R2 ? +R2.width.toFixed(1) : null, logoLeftPct: R2 ? +(R2.left / innerWidth * 100).toFixed(2) : null,
            ctaW: R3 ? +R3.width.toFixed(1) : null, ctaRightPct: R3 ? +((innerWidth - R3.right) / innerWidth * 100).toFixed(2) : null,
            navFont: nav ? getComputedStyle(nav.querySelector('a') || nav).fontSize : null});
        })()
        """
        live = json.loads((await send("Runtime.evaluate", {"expression": js, "returnByValue": True}))["result"]["value"])
    print("الهيدر الحيّ:", json.dumps(live, ensure_ascii=False))

    for k in STRIPS:
        im = Image.open(OUT / f"{k}.png").convert("RGB")
        a = np.asarray(im).astype(int)
        W = a.shape[1]
        # الحبر = البكسلات التي تختلف عن خلفية الشريط (أول بكسل يسار أعلى)
        bg = a[2, 2]
        ink = (np.abs(a - bg).max(axis=2) > 26)
        cols = ink.any(axis=0)
        rows = ink.any(axis=1)
        xs = np.where(cols)[0]
        ys = np.where(rows)[0]
        if len(xs) == 0:
            print(f"{k}: ما في حبر مقروء")
            continue
        # مجمّعات أفقية (فجوات > 20px)
        groups, start = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] - xs[i - 1] > 20:
                groups.append((start, xs[i - 1]))
                start = xs[i]
        groups.append((start, xs[-1]))
        print(f"\n{k} ({W}px): حبر من {xs[0]} إلى {xs[-1]}  ·  ارتفاع الحبر {ys[0]}→{ys[-1]}")
        print(f"   هامش يسار {xs[0]/W*100:.2f}%  ·  هامش يمين {(W-1-xs[-1])/W*100:.2f}%")
        for gi, (g0, g1) in enumerate(groups[:8]):
            print(f"   مجموعة {gi+1}: x {g0}→{g1}  ({(g1-g0+1)/W*100:.1f}% من العرض)")


asyncio.run(main())
