import asyncio
import logging
import random
import re
import time
from traceback import format_tb

from playwright.async_api import async_playwright
import Func_Lib as Lib

infos = []
ativo = False


async def is_placar(string):
    reg_exp = r"\d+"
    return re.match(reg_exp, string)


async def normal_monit(pagina):
    fato = ""
    red_casa = 0
    amarelo_casa = 0
    red_fora = 0
    amarelo_fora = 0
    cantos_casa = 0
    cantos_fora = 0
    stats_p = ""

    score = await pagina.locator(".scoreboard__top").inner_text()
    score_splt = score.split("\n")
    await pagina.wait_for_selector(".live-incidents__container__title")
    drop = pagina.locator(".live-incidents__container__title")
    await drop.click()
    await pagina.wait_for_selector(".sb-dropdown--extended")
    incidents = await pagina.locator(".sb-dropdown--extended").inner_text()
    incidents = incidents.split("\n")

    for ind, inc in enumerate(incidents):
        if await Lib.is_tempo(inc):
            incidents[ind] = incidents[ind].replace("'", "")

    for ind, inc in enumerate(incidents):
        if inc == "Pênalti perdido" and not incidents[ind - 1].isdigit():
            incidents.insert(ind, incidents[ind + 1])
        if inc == incidents[0]:
            incidents[ind] = f"Gol! - {incidents[0]}"
        if inc == incidents[5]:
            incidents[ind] = f"Gol! - {incidents[5]}"

    for i, inc in enumerate(incidents):
        if "cartão amarelo" in inc:
            if score_splt[0] in incidents[i]:
                amarelo_casa += 1
            else:
                amarelo_fora += 1
            logging.info(f"Peguei um cartão amarelo nos incidentes: {inc}")
        elif "cartão vermelho" in inc:
            if score_splt[0] in incidents[i]:
                red_casa += 1
            else:
                red_fora += 1
            logging.info(f"Peguei um cartão vermelho nos incidentes: {inc}")

        if "escanteio" in inc:
            if score_splt[0] in incidents[i]:
                cantos_casa += 1
            else:
                cantos_fora += 1
            logging.info(f"Peguei um escanteio nos incidentes: {inc}")

    await pagina.wait_for_selector(".control-button")
    control = pagina.locator(".control-button")
    btn_state = await control.nth(4).get_attribute("class")
    if "active" not in btn_state:
        await control.nth(4).click()
        print("Ativei o Botao!")
    try:
        await pagina.wait_for_selector("role=tab")
    except TimeoutError:
        await control.nth(4).click()
        await pagina.wait_for_selector("role=tab")
    print("Monitorando normalmente")
    l_crono = pagina.locator('role=tab')
    await l_crono.nth(1).click()
    await asyncio.sleep(3)
    await pagina.wait_for_selector(".sr-lmt-plus-1-detailed-statistics__content")
    estatisticas = await pagina.locator(
        ".sr-lmt-plus-1-detailed-statistics__content").inner_text()
    stats = estatisticas.split("\n")

    stats_p = stats_p + f'''
🟨 Cartões Amarelos:\n
{score_splt[0]} - {amarelo_casa}
{score_splt[5]} - {amarelo_fora}\n
🟥 Cartões Vermelhos:\n
{score_splt[0]} - {red_casa}
{score_splt[5]} - {red_fora}\n
⛳️ Escanteios:\n                                                             
{score_splt[0]} - {cantos_casa}                                             
{score_splt[5]} - {cantos_fora}\n'''

    if stats:

        for i in range(len(stats)):
            if stats[i] == "OPORTUNIDADES DE GOLO":
                stats_p = stats_p + f'''
❌🥅 Oportunidades de gol:\n
{score_splt[0]} - {stats[i - 1]} 
{score_splt[5]} - {stats[i + 1]}\n'''
                # print(f"Stats refinado: \n{stats_p}")
            if stats[i] == "REMATES À BALIZA":
                stats_p = stats_p + f'''
👟 🥅 Chutes ao gol:\n                                                         
{score_splt[0]} - {stats[i - 1]}                                             
{score_splt[5]} - {stats[i + 1]}\n'''
                # print(f"Stats refinado: \n{stats_p}")

            if stats[i] == "POSSE DE BOLA":
                stats_p = stats_p + f'''
⚽️ Posse de Bola:\n                                                                 
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''
                # print(f"Stats refinado: \n{stats_p}")
            if stats[i] == "ATAQUE PERIGOSO":
                stats_p = stats_p + f'''
🎯 Ataque Perigoso:\n                                                               
{score_splt[0]} - {stats[i - 1]}                                                   
{score_splt[5]} - {stats[i + 1]}\n'''
                # print(f"Stats refinado: \n{stats_p}")
            if stats[i] == "ATAQUE":
                stats_p = stats_p + f'''
🎯 Ataque:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''

            if stats[i] == "BOLA SEGURA":
                stats_p = stats_p + f'''
⚽️ Bola Segura:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''

            if stats[i] == "DEFESAS":
                stats_p = stats_p + f'''
🥅🎯 Defesas:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''

            if stats[i] == "FORAS DE JOGO":
                stats_p = stats_p + f'''
⛔️⚽️ Impedimentos:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''

            if stats[i] == "FALTAS":
                stats_p = stats_p + f'''
✖️⚽️ Faltas:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[5]} - {stats[i + 1]}\n'''

    stats_now = f'''<b>\n
⚽️ {score_splt[0]} {score_splt[2]} x {score_splt[4]} {score_splt[5]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n                                                                                                                                 
'''
    return stats_now


async def monitorar():
    async with async_playwright() as p:
        try:
            while ativo:
                browser = await p.chromium.launch(headless=False)
                pagina = await browser.new_page()
                await pagina.goto("https://br.betano.com/live/")

                t_inicial = time.time()

                try:

                    if pagina.expect_popup(timeout=0):
                        await pagina.keyboard.press("Escape")
                except Exception as error:
                    print(f"Time out exception!\n{error}")

                btn_fut = pagina.locator("[aria-label='Select category FUTEBOL']")
                await btn_fut.click()

                match = pagina.locator('.live-events-event-row__main')
                await match.nth(0).click()

                await pagina.wait_for_selector(".scoreboard__top")

                qtd = "0"
                qtd_rows = "1"
                while qtd != qtd_rows:

                    quant_jg = pagina.locator("text=Jogos ao Vivo (")
                    quant_jg = await quant_jg.inner_text()
                    print(quant_jg)
                    match = pagina.locator('.live-events-event-row__main')
                    qtd = re.search(r"\d+", quant_jg)
                    qtd = int(qtd.group())
                    qtd_rows = await match.count()
                    print(qtd)
                    print(qtd_rows)
                    t_final = time.time()
                    if t_final - t_inicial > 120:
                        print(f"Demorou tempo demais, vou fazer assim mesmo!")
                        qtd_rows = qtd

                else:
                    print("Farei a rotina porque igualou!")
                    qtd_fut = pagina.locator(r"text=Futebol (")
                    qtd_fut = await qtd_fut.inner_text()
                    qtd_fut = re.search(r"\d+", qtd_fut)
                    qtd_fut = int(qtd_fut.group())
                    print(qtd_fut)
                    texto = ""
                    for i in range(qtd_fut):
                        await match.nth(i).hover(timeout=0, force=True)
                        await match.nth(i).click()
                        if "(Esports)" not in await match.nth(i).inner_text():
                            if "(Simulação)" not in await match.nth(i).inner_text():
                                await pagina.wait_for_selector(".scoreboard__top")
                                score = await pagina.locator(".scoreboard__top").inner_text()
                                score_splt = score.split("\n")
                                casa = score_splt[0]
                                fora = score_splt[-1]
                                while casa not in await match.nth(i).inner_text():
                                    score = await pagina.locator(".scoreboard__top").inner_text()
                                    score_splt = score.split("\n")
                                    casa = score_splt[0]

                                fora = score_splt[-1]
                                tempo = score_splt[-5]

                                if await is_placar(score_splt[-2]) and score_splt[-3] == "-":
                                    print("Confirmei e é jogo!")
                                else:
                                    break

                                if tempo == "0:00":
                                    print("O jogo ainda não começou!")
                                    continue

                                await pagina.wait_for_selector(".control-events-title")
                                event = await pagina.locator(".control-events-title").inner_text()

                                if f"{casa} - {fora}" == event:
                                    print("Vou monitorar de forma normal")
                                    res_monit = await normal_monit(pagina)

                                else:
                                    print("Vou monitorar de forma alternativa")

                                texto = texto + await match.nth(i).inner_text() + "\n" + "fim_jogo" + "\n"

                                if not ativo:
                                    break

                                await trigger(res_monit)

                await browser.close()
                await asyncio.sleep(random.randrange(300, 600))

        except Exception as error:
            print(f"Deu merda, aqui o que foi: {error.__class__}")
            print(error)
            print(format_tb(error.__traceback__))


async def trigger(info):
    infos.append(info)
    logging.info(f"Ativei o trigger, ta ai a info:\n{info}")
    print("Adicionei uma atualização!")
