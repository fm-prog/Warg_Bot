from playwright.async_api import async_playwright
import re
import time
import logging
from traceback import format_tb
import Func_Lib as Lib


class MotorLive:

    @staticmethod
    async def mostrar_jogos_live():
        async with async_playwright() as p:
            done = False
            while not done:
                try:
                    ligas = []
                    lst_live = []
                    texto = ""
                    browser = await p.chromium.launch(headless=False)
                    page = await browser.new_page()
                    await page.goto("https://br.betano.com/live/")
                    t_inicial = time.time()

                    if page.expect_popup():
                        await page.keyboard.press("Escape")

                    btn_fut = page.locator("[aria-label='Select category FUTEBOL']")
                    await btn_fut.click()

                    qtd = "0"
                    qtd_rows = "1"

                    while qtd != qtd_rows:
                        quant_jg = await page.locator(".live-events__sport-name").text_content()
                        match = page.locator('.live-events-event-row__main')
                        qtd = re.search(r"\d+", quant_jg)
                        qtd = int(qtd.group())
                        qtd_rows = await match.count()
                        t_final = time.time()
                        if t_final - t_inicial > 120:
                            break
                    else:
                        logging.info(f"Farei a rotina porque igualou!")
                        print("Farei a rotina porque igualou!")

                        for i in range(await match.count()):
                            await match.nth(i).hover(timeout=0, force=True)
                            if "(Esports)" not in await match.nth(i).inner_text():
                                if "(Simulação)" not in await match.nth(i).inner_text():
                                    texto = texto + await match.nth(i).inner_text() + "fim_jogo"

                        jogos_live = texto.split("fim_jogo")

                        for i in jogos_live:
                            ligas.append(i.split("\n"))

                        qtd_jogos_live = len(ligas) - 1

                        ao_vivo = f"\n🏟 <b>Ao vivo: {qtd_jogos_live}</b>\n"

                        for e in range(len(ligas)):

                            for i in range(len(ligas[e])):

                                if await Lib.is_horario(ligas[e][i]):

                                    if await Lib.is_prolongamento(ligas[e][i + 1]):
                                        ao_vivo = ao_vivo + f"\n⚽️ <b>{ligas[e][i + 2]} {ligas[e][i + 4]} ✖️ {ligas[e][i + 5]} {ligas[e][i + 3]}</b>\n"
                                        ao_vivo = ao_vivo + f"⌛️ <b>{ligas[e][i + 0]} 🕐 {ligas[e][i + 1]}</b>\n"
                                    else:
                                        ao_vivo = ao_vivo + f"\n⚽️ <b>{ligas[e][i + 1]} {ligas[e][i + 3]} ✖️ {ligas[e][i + 4]} {ligas[e][i + 2]}</b>\n"
                                        ao_vivo = ao_vivo + f"⌛️ <b>{ligas[e][i + 0]}</b>\n"
                                    if len(ao_vivo) > 3000:
                                        lst_live.append(ao_vivo)
                                        ao_vivo = ""
                        t_final = time.time()
                        logging.info(f"Demorei {t_final - t_inicial} para retornar os jogos!")
                        print(f"Demorei {t_final - t_inicial} para retornar os jogos!")
                        lst_live.append(ao_vivo)
                        await browser.close()
                        return lst_live
                    logging.info(f"Demorou mais do que o necessário, vou tentar novamente!")
                    print("Demorou mais que o necessário, vou tentar novamente!")
                except Exception as error:
                    print(f"Deu merda, aqui o que foi: {error.__class__}")
                    print(error)
                    print(format_tb(error.__traceback__))
                    info = f'''
    Deu merda, aqui no Tryzão, o que foi: {error.__class__}\n
    {error}\n
    {format_tb(error.__traceback__)}\n
    '''
                    await browser.close()
                    logging.error("Deu erro na busca dos jogos ao vivo!")
                    logging.info("Vou tentar de novo!")
                    logging.error(info)
