import asyncio
from playwright.async_api import async_playwright
URL="http://localhost:5173/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1440,"height":1100})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL+"#/week/5", wait_until="networkidle"); await pg.wait_for_timeout(700)
        # open explain on first snippet
        await pg.locator(".explain-toggle").first.click(); await pg.wait_for_timeout(400)
        print("annot rows:", await pg.locator(".annot-row").count())
        print("explain text:", (await pg.locator(".explain-text").first.inner_text())[:110])
        await pg.screenshot(path="/home/user/shots/30-week-explain.png", full_page=True)
        # drill step 1
        await pg.goto(URL+"#/drill/w05-01", wait_until="networkidle"); await pg.wait_for_timeout(600)
        print("drill annot:", await pg.locator(".annot-row").count(), "| gotcha:", await pg.locator(".gotcha").count())
        await pg.screenshot(path="/home/user/shots/31-drill-explain.png", full_page=True)
        # code tab
        await pg.locator(".segmented button", has_text="Code").first.click(); await pg.wait_for_timeout(300)
        await pg.screenshot(path="/home/user/shots/32-drill-code-tab.png")
        # pass recall to see post-pass explanation
        await pg.locator(".segmented button", has_text="Explained").first.click()
        code = "import pandas as pd\n\ndf = pd.read_csv(\"data.csv\")\nprint(df.shape)"
        ta = pg.locator(".typer-input").first
        for _ in range(3):
            await ta.click(); await pg.keyboard.type(code, delay=3); await pg.wait_for_timeout(300)
        await pg.wait_for_timeout(1100)
        ta = pg.locator(".typer-input").first
        await ta.click(); await pg.keyboard.type(code, delay=3)
        await pg.locator("button", has_text="Submit recall").click(); await pg.wait_for_timeout(1000)
        print("post-pass explain panels:", await pg.locator(".result-explain .annot").count())
        await pg.screenshot(path="/home/user/shots/33-pass-explain.png", full_page=True)
        await b.close()
        print("errors:", errs)
asyncio.run(main())
