import asyncio
import datetime
import re
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://br.betano.com/live/hapoel-kfar-shelem-shimshon-kfar-qasem/30482011/")

        if page.expect_popup(timeout=0):
            await page.keyboard.press("Escape")

        # await page.wait_for_selector(".stats-tracker")
        # frame = page.frame_locator(".js-iframe-container")
        await asyncio.sleep(10)
        frames = page.frames

        for ind, i in enumerate(frames):
            if "wab" in str(i):
                frame = frames[ind]
                # await frame.locator(".commentary").click()
                frame = frame.locator(".stats-tracker")
                btns = frame.locator(".icon")
                frame = frame.locator(".visuallyhidden")
                #frame = frame.locator(".icon.icon-tables")
                #await frame.click()
                #print(await frame.text_content())
                for btn in range(await frame.count()):
                    await btns.nth(btn).click()
                    #lista = await frame.nth(btn).text_content()
                    #print(lista.split("\n"))
                    await asyncio.sleep(3)

                #print(await frame.locator(".visuallyhidden").all_text_contents())

        # frame2 = page.frame_locator('wab')

        # await page.wait_for_selector('.js-iframe-container')

        # print(frame2)
        # frame1 = page.frame_locator('iframe').first.locator('iframe').nth(1).locator(".stats-tracker")

        # print(await frame1.inner_html())

        # await frame1.locator(".liveMatch").click()


if __name__ == '__main__':
    asyncio.run(main())
