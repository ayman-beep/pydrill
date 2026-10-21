import asyncio
from playwright.async_api import async_playwright
URL="http://localhost:5173/"
SEED = """() => {
  const now = new Date(); const key = d => d.toISOString().slice(0,10);
  const state = {version:1, created:key(now), cards:{}, xp:1840, streak:{current:6,best:9,lastDay:key(now)}, daily:{}, sessions:[], settings:{sound:true,strict:true,tts:false}};
  let i=0; for (const w of [1,2,3,5,8,10]) for (let k=1;k<=6;k++) {
    const id = `w${String(w).padStart(2,'0')}-0${Math.min(k,9)}`;
    const stage=(i*3)%7; const d=new Date(now); d.setDate(d.getDate()+((i%5===0)?-1:(i%7)));
    state.cards[id]={stage,ease:2.5,due:key(d),lapses:i%3,reps:2,typeRuns:4,recallAttempts:2,needsTyping:false,lastReviewed:key(now),history:[]}; i++; }
  for (let d=0; d<22; d++){ const dd=new Date(now); dd.setDate(dd.getDate()-d);
    state.daily[key(dd)]={reviews:(d*3)%11, typingRuns:(d*2)%7, keystrokes:(d*37)%400, recalls:(d*2)%6, exact:d%3}; }
  localStorage.setItem('pydrill.progress.v1', JSON.stringify(state));
}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        page=await b.new_page(viewport={"width":1440,"height":1000})
        errors=[]
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(URL, wait_until="networkidle"); await page.evaluate(SEED); await page.reload(wait_until="networkidle")
        await page.wait_for_timeout(700)
        await page.screenshot(path="/home/user/shots/20-dashboard.png", full_page=True)
        await page.goto(URL+"#/week/5", wait_until="networkidle"); await page.wait_for_timeout(500)
        await page.screenshot(path="/home/user/shots/21-week.png", full_page=True)
        await page.goto(URL+"#/stats", wait_until="networkidle"); await page.wait_for_timeout(500)
        await page.screenshot(path="/home/user/shots/22-stats.png", full_page=True)
        # drill a card whose stage>0 -> recall directly; show wrong-answer diff
        await page.goto(URL+"#/drill/w05-01", wait_until="networkidle"); await page.wait_for_timeout(600)
        print("phase recall?", await page.locator(".prompt-text").count())
        ta = page.locator(".typer-input").first
        await ta.click(); await page.keyboard.type('import pandas as pd\ndf = pd.read_csv("data.csv")\nprint(df.size)', delay=3)
        await page.locator("button", has_text="Submit recall").click(); await page.wait_for_timeout(900)
        await page.screenshot(path="/home/user/shots/23-diff.png", full_page=True)
        m=await b.new_page(viewport={"width":390,"height":844}); await m.goto(URL, wait_until="networkidle"); await m.evaluate(SEED); await m.reload(wait_until="networkidle"); await m.wait_for_timeout(600)
        await m.screenshot(path="/home/user/shots/24-mobile.png", full_page=True)
        await m.goto(URL+"#/drill/w05-01", wait_until="networkidle"); await m.wait_for_timeout(600)
        await m.screenshot(path="/home/user/shots/25-mobile-drill.png", full_page=True)
        print("ERRORS:", errors)
        await b.close()
asyncio.run(main())
