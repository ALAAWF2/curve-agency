"""1) make .hero-lead use the 55% grey like every other section body,
   2) render the COMPANY PROFILE cover (assets/page1.svg) as a work-card image,
   3) append it to the portfolio grid as a 13th card."""
import asyncio, base64, json, time, urllib.request
from pathlib import Path
import websockets

R = Path(r"C:/Users/Orange/workspace/curve-site")

# ---- 1) .hero-lead out of the small-label grey list ----
C = R / "styles.css"
css = C.read_text(encoding="utf-8")
css = css.replace(".service-num, .step-num, .stat-label, .hero-lead, .card-caption, .mobile-contact-line,",
                  ".service-num, .step-num, .stat-label, .card-caption, .mobile-contact-line,")
C.write_text(css, encoding="utf-8")
print("✓ .hero-lead removed from the small-label grey list")

# ---- 2) render the cover ----
PNG = R / "assets" / "web" / "work-company-profile.png"


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
        await send("Emulation.setDeviceMetricsOverride",
                   {"width": 1600, "height": 900, "deviceScaleFactor": 1, "mobile": False})
        await send("Page.navigate", {"url": "http://127.0.0.1:8080/assets/page1.svg"})
        await asyncio.sleep(3)
        shot = await send("Page.captureScreenshot", {"format": "png"})
        PNG.write_bytes(base64.b64decode(shot["data"]))
        print(f"✓ {PNG.name} ({PNG.stat().st_size} بايت)")


asyncio.run(main())

# ---- 3) الكرت الجديد ----
H = R / "index.html"
h = H.read_text(encoding="utf-8")
CARD = """
          <!-- Work 13: CURVE Company Profile (the identity in application) -->
          <article class="work-card" data-category="branding identity" data-index="13">
            <div class="work-visual">
              <img src="assets/web/work-company-profile.png" alt="CURVE Company Profile cover" class="work-img" loading="lazy">
            </div>
            <div class="work-info">
              <div class="work-badge">BRAND DOCUMENT</div>
              <span class="work-client">CURVE</span>
              <h3 class="work-title">COMPANY PROFILE — IDENTITY IN APPLICATION</h3>
              <p class="work-desc">
                The agency's own profile deck: the wordmark, the geometric element set and the black-and-white
                system carried across print, stationery, merchandise and digital touchpoints.
              </p>
            </div>
          </article>
"""
if "work-company-profile.png" not in h:
    end = h.find("</div>", h.find('id="work-grid"'))
    # نُلحق الكرت قبل إغلاق شبكة الأعمال: نبحث عن آخر </article> داخل الشبكة
    grid_start = h.find('id="work-grid"')
    grid_end = h.find("</section>", grid_start)
    last_article = h.rfind("</article>", grid_start, grid_end)
    ins = last_article + len("</article>")
    h = h[:ins] + CARD + h[ins:]
    H.write_text(h, encoding="utf-8")
    print("✓ كرت COMPANY PROFILE أُضيف إلى شبكة الأعمال")
else:
    print("· الكرت موجود مسبقاً")
print("   عدد كروت work-card:", h.count('class="work-card"'))
