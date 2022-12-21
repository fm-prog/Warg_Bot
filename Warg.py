import asyncio
import logging
import time
from playwright.async_api import async_playwright
from traceback import format_tb
import re
from Monitor import Watcher
import Func_Lib as Lib

infos = []
paginas = []
monitorados = ["Stand By", "Stand By", "Stand By", "Stand By", "Stand By"]
low_mem = False


async def obs_check():
    for i in monitorados:
        if i == "Stand By":
            return True


async def torcer(jogo):
    obs = await obs_check()
    if obs:
        async with async_playwright() as p:
            alternativo = True
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://br.betano.com/live/")
            t_inicial = time.time()

            try:

                if page.expect_popup(timeout=0):
                    await page.keyboard.press("Escape")
            except Exception as error:
                print(f"Time out exception!\n{error}")

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
                    print(f"Demorou tempo demais, vou fazer assim mesmo!")
                    logging.info(f"Demorou tempo demais, vou fazer assim mesmo!")
                    break
            else:
                logging.info("Farei a rotina de pesquisa dos jogos porque igualou!")
                print("Farei a rotina porque igualou!")

            try:

                for i in range(await match.count()):
                    await match.nth(i).hover()
                    match.nth(i)
                    times = await match.nth(i).inner_text()
                    times = times.split("\n")

                    for t in times:
                        if "Simulação" not in t:
                            if "Esports" not in t:
                                logging.info(t)
                                evid = await Lib.longestsubstring(jogo.lower(), t.lower())
                                if evid:
                                    t_final = time.time()
                                    print(f"Demorei {t_final - t_inicial} para achar!")
                                    logging.info(f"Demorei {t_final - t_inicial} para achar!")
                                    html = await match.nth(i).inner_html()
                                    await match.nth(i).click()
                                    score = await page.locator(".scoreboard__top").inner_text()
                                    score_splt = score.split("\n")
                                    print(score_splt)

                                    tempo = score_splt[-5]
                                    casa = score_splt[0]
                                    fora = score_splt[-1]
                                    p_casa = score_splt[-4]
                                    p_fora = score_splt[-2]

                                    if tempo == "0:00":
                                        logging.info("O jogo ainda não começou!")
                                        return "O jogo ainda não começou!"

                                    #await page.wait_for_selector(".live-incidents__container__title")

                                    stats_now = f'''<b>⚽️ {casa} {p_casa} x {p_fora} {fora}\n
⌛️ {tempo}\n</b>'''

                                    await page.wait_for_selector(".control-events-title")
                                    await page.locator(".control-events-title").click()
                                    await page.wait_for_selector(".dropdown-item")
                                    drop = page.locator(".dropdown-item")

                                    for d in range(await drop.count()):
                                        if await drop.nth(d).inner_text() == f"{casa} - {fora}":
                                            alternativo = False
                                            print("Vou monitorar de forma normal!")
                                            logging.info("Vou monitorar de forma normal!")
                                            break

                                    print(stats_now)
                                    logging.info(f"Achei o jogo!\n{stats_now}")
                                    html = html.split('"')
                                    for a, elemento in enumerate(html):
                                        if "href" in elemento:
                                            href = html[a + 1]
                                            break

                                    for pag in paginas:
                                        if pag == href:
                                            logging.info("Este jogo já está sendo monitorado!")
                                            return "Este jogo já está sendo monitorado!"

                                    paginas.append(href)
                                    print(href)

                                    observ = 0
                                    for ind, m in enumerate(monitorados):
                                        if m == "Stand By":
                                            observ = ind
                                            monitorados[ind] = stats_now
                                            break

                                    if alternativo:
                                        print("Vou monitorar de forma alternativa!")
                                        logging.info("Vou monitorar de forma alternativa!")
                                        stats_now += "\n<b>⚠️ Cobertura da Partida Limitada!</b>\n"

                                    await browser.close()
                                    monitor = Watcher()
                                    asyncio.create_task(monitor.monitorar(href, alternativo, observ, low_mem))
                                    return stats_now

                await browser.close()
                logging.error(f"Foi mal, não encontrei o jogo! {jogo}")
                return f"Foi mal, não encontrei o jogo!\n\nTem certeza que já começou?\n\nVê se tu escreveu o nome do " \
                       f"time certo! "

            except Exception as error:
                await browser.close()
                print(f"Deu merda, aqui o que foi: {error.__class__}")
                print(error)
                print(format_tb(error.__traceback__))
                info = f'''
    Deu merda, aqui no Tryzão, o que foi: {error.__class__}\n
    {error}\n
    {format_tb(error.__traceback__)}\n
    '''
                logging.error(info)
                return "Foi mal, tive um problema ao procurar!\nTenta me dizer de novo!"
    else:
        logging.error("Todos os observadores estão ocupados!")
        return "Todos os observadores estão ocupados!"


async def trigger(info):
    infos.append(info)
    logging.info(f"Ativei o trigger, ta ai a info:\n{info}")
    print("Adicionei uma atualização!")
