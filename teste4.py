import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        alternativo = True
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://br.betano.com/live/as-douanes-fc-nouadhibou/30726888/")

        try:

            if page.expect_popup(timeout=0):
                await page.keyboard.press("Escape")
        except Exception as error:
            print(f"Time out exception!\n{error}")

        await page.wait_for_selector(".control-events-title")
        locator = page.locator(".control-events-title")
        print(await locator.inner_text())
        print(await locator.inner_html())


if __name__ == '__main__':
    asyncio.run(main())
