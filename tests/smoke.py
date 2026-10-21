"""End-to-end walkthrough of the drill pipeline (needs the app running).

    python3 tests/smoke.py            # app on :5173, API on :8000
"""
import asyncio, json, urllib.request
from playwright.async_api import async_playwright

URL = "http://localhost:5173/"
API = "http://localhost:8000/api"


def snippet(sid):
    return json.loads(urllib.request.urlopen(f"{API}/snippets/{sid}").read())


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1440, "height": 1000})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(600)
        print("dashboard weeks:", await page.locator(".week-card").count())

        # ---- week view + inline explanation
        await page.locator(".week-card").first.click()
        await page.wait_for_timeout(400)
        await page.locator(".explain-toggle").first.click()
        await page.wait_for_timeout(300)
        print("week: annotated rows =", await page.locator(".annot-row").count())
        print("week: explanation   =", (await page.locator(".explain-text").first.inner_text())[:70], "…")

        # ---- drill step 1/2
        snip = snippet("w01-01")
        code = snip["code"]
        await page.locator(".snippet-item").first.locator("button", has_text="Learn").click()
        await page.wait_for_timeout(600)
        print("drill:", await page.locator(".drill-title h1").first.inner_text())
        print("drill: notes per line =", await page.locator(".annot-row").count(), "/ code lines", snip["lines"])
        print("drill: common mistake shown =", await page.locator(".gotcha").count() == 1)

        ta = page.locator(".typer-input").first
        for run in range(3):
            await ta.click()
            await page.keyboard.type(code, delay=2)
            await page.wait_for_timeout(250)
            print(f"  run {run + 1}: filled dots = {await page.locator('.run-dot.filled').count()}")

        # ---- strict-mode error reset
        await page.wait_for_timeout(1200)
        print("recall phase reached:", await page.locator(".prompt-text").count() == 1)

        ta2 = page.locator(".typer-input").first
        await ta2.click()
        await page.keyboard.type("print('wrong answer')", delay=2)
        await page.locator("button", has_text="Submit recall").click()
        await page.wait_for_timeout(800)
        print("wrong answer ->", await page.locator(".result").get_attribute("class"))
        print("diff rows:", await page.locator(".diff-row").count())

        # ---- lapse forces step 1 again
        await page.locator("button", has_text="Repeat 3× typing drill").click()
        await page.wait_for_timeout(500)
        print("back at typing, dots reset:", await page.locator(".run-dot.filled").count())

        for _ in range(3):
            await ta.click()
            await page.keyboard.type(code, delay=2)
            await page.wait_for_timeout(250)
        await page.wait_for_timeout(1100)
        ta2 = page.locator(".typer-input").first
        await ta2.click()
        await page.keyboard.type(code, delay=2)
        await page.locator("button", has_text="Submit recall").click()
        await page.wait_for_timeout(900)
        print("correct ->", await page.locator(".result").get_attribute("class"))
        print("post-pass explanation:", await page.locator(".result-explain .annot-row").count(), "annotated lines")

        store = json.loads(await page.evaluate("localStorage.getItem('pydrill.progress.v1')"))
        card = store["cards"]["w01-01"]
        print("card:", {k: card[k] for k in ("stage", "due", "lapses", "typeRuns", "reps")})
        print("xp:", store["xp"], "streak:", store["streak"]["current"])

        await page.goto(URL, wait_until="networkidle")
        await page.wait_for_timeout(500)
        print("mastery:", await page.locator(".hero-ring .ring-center strong").inner_text())
        await page.goto(URL + "#/stats", wait_until="networkidle")
        await page.wait_for_timeout(400)
        print("stats rows:", await page.locator(".card-row").count())
        print("ERRORS:", errors or "none")
        await b.close()


asyncio.run(main())
