import asyncio
import datetime
import re
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://br.betano.com/live/us-grosseto-ghivizzano-borgoamozzano/30506699/")
        sum = ""
        if page.expect_popup(timeout=0):
            await page.keyboard.press("Escape")

        await page.wait_for_selector(".control-button")
        control = page.locator(".control-button")
        btn_state = await control.nth(4).get_attribute("class")
        if "active" not in btn_state:
            await control.nth(4).click()
            print("Ativei o Botao!")
            await asyncio.sleep(2)

        frames = page.frames
        print(f"Total de frames:{len(frames)}")




                        #icon = stats.locator(".icon")
        #print(await cw.count())
        #for ind in range(await cw.count()):
        #    await asyncio.sleep(2)
        #    await cw.nth(ind).inner_text()
        #    cw = stats.locator(".custom-widget")
        #    print(await cw.nth(ind).inner_text())
        # print(frames)
        # for ind, i in enumerate(frames):
        # if "api" in str(i):
        # frame = frames[ind]
        # await frame.locator(".stats-tracker").click()
        # await frame.wait_for_selector(".stats-tracker")
        # print(await frame.inner_html(".icon"))
        # print(await frame.content())
        # break
        # frame = frame.locator(".stats-tracker")
        # btns = frame.locator(".icon")
        # frame = frame.locator(".visuallyhidden")
        # frame = frame.locator(".icon.icon-tables")
        # await frame.click()
        # print(await frame.text_content())
        # for btn in range(await frame.count()):
        # await btns.click()
        # lista = await frame.nth(btn).text_content()
        # print(lista.split("\n"))
        # await asyncio.sleep(3)

        # print(await frame.locator(".visuallyhidden").all_text_contents())

        # frame2 = page.frame_locator('wab')

        # await page.wait_for_selector('.js-iframe-container')

        # print(frame2)
        # frame1 = page.frame_locator('iframe').first.locator('iframe').nth(1).locator(".stats-tracker")

        # print(await frame1.inner_html())

        # await frame1.locator(".liveMatch").click()


if __name__ == '__main__':
    asyncio.run(main())
