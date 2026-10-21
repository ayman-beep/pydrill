"""Verifies the fully static build with the API server stopped.

    npm run build && npx vite preview --port 4173   (then)
    python3 tests/static_smoke.py
"""
import asyncio, json
from playwright.async_api import async_playwright

URL = "http://localhost:4173/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1440, "height": 1000})
        errors, api_calls, requests = [], [], []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("request", lambda r: (requests.append(r.url),
                                      api_calls.append(r.url) if "/api/" in r.url else None))
        page.on("requestfailed", lambda r: errors.append(f"FAILED {r.url}"))

        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(600)
        print("title           :", await page.title())
        print("week cards      :", await page.locator(".week-card").count())
        print("due chip        :", await page.locator(".chip-btn.due").inner_text())

        # week view + explanation
        await page.locator(".week-card").first.click(); await page.wait_for_timeout(400)
        await page.locator(".explain-toggle").first.click(); await page.wait_for_timeout(300)
        print("annotated rows  :", await page.locator(".annot-row").count())

        # full drill: 3 perfect runs -> recall
        code = "name = \"Ada\"\nage = 28\nprint(name, age)"
        await page.locator(".snippet-item").first.locator("button", has_text="Learn").click()
        await page.wait_for_timeout(500)
        ta = page.locator(".typer-input").first
        for i in range(3):
            await ta.click(); await page.keyboard.type(code, delay=2); await page.wait_for_timeout(250)
        print("runs completed  :", await page.locator(".run-dot.filled").count())
        await page.wait_for_timeout(1200)

        # failing recall -> local diff
        ta2 = page.locator(".typer-input").first
        await ta2.click(); await page.keyboard.type('print("nope")', delay=2)
        await page.locator("button", has_text="Submit recall").click(); await page.wait_for_timeout(600)
        print("wrong -> result :", await page.locator(".result").get_attribute("class"))
        print("diff rows       :", await page.locator(".diff-row").count())

        # recovery + pass
        await page.locator("button", has_text="Repeat 3× typing drill").click(); await page.wait_for_timeout(400)
        for i in range(3):
            await ta.click(); await page.keyboard.type(code, delay=2); await page.wait_for_timeout(250)
        await page.wait_for_timeout(1100)
        ta2 = page.locator(".typer-input").first
        await ta2.click(); await page.keyboard.type(code, delay=2)
        await page.locator("button", has_text="Submit recall").click(); await page.wait_for_timeout(600)
        print("correct -> result:", await page.locator(".result").get_attribute("class"))

        store = json.loads(await page.evaluate("localStorage.getItem('pydrill.progress.v1')"))
        print("card state      :", {k: store["cards"]["w01-01"][k] for k in ("stage", "due", "lapses")})
        print("post-pass notes :", await page.locator(".result-explain .annot-row").count())

        await page.goto(URL + "#/stats", wait_until="networkidle"); await page.wait_for_timeout(400)
        print("stats rows      :", await page.locator(".card-row").count())

        print()
        print("network requests:", len(requests), "(all same-origin static assets)")
        print("API calls       :", api_calls or "NONE ✓")
        print("errors          :", errors or "none ✓")
        await b.close()

asyncio.run(main())
