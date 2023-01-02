import asyncio
import logging
import random
import re
import time
# from random import random
from traceback import format_tb
from Data_Aposta import Inter_csv
from playwright.async_api import async_playwright
import Func_Lib as Lib

infos = []
ativo = False
soloq_jogos = asyncio.Queue()
Observers = ["Stand By", "Stand By", "Stand By", "Stand By"]


async def is_placar(string):
    reg_exp = r"\d+"
    return re.match(reg_exp, string)


async def initial_monit(pagina):
    red_casa = 0
    amarelo_casa = 0
    red_fora = 0
    amarelo_fora = 0
    cantos_casa = 0
    cantos_fora = 0
    stats_p = ""
    expected = "Nan"

    score = await pagina.locator(".scoreboard__top").inner_text()
    score_splt = score.split("\n")

    try:
        await pagina.wait_for_selector(".scoreboard-summary__item.expected-goal.swiper-slide.has-tooltip", timeout=2000)
        expected = await pagina.locator(".scoreboard-summary__item.expected-goal.swiper-slide.has-tooltip").inner_text()
        expected = expected.split("-")

    except Exception as error:
        if "Timeout" in str(error):
            print(f"Exception forçada com sucesso devido à ausência de XG!")
        else:
            print(f"Deu merda, aqui o que foi: {error.__class__}")
            print(error)
            print(format_tb(error.__traceback__))

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
        if inc == score_splt[0]:
            incidents[ind] = f"Gol! - {score_splt[0]}"
        if inc == score_splt[-1]:
            incidents[ind] = f"Gol! - {score_splt[-1]}"

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

    print(f"Esperado: {expected}")
    if expected != "Nan":
        print("Coloquei expected")
        stats_p = stats_p + f'''Cartões Amarelos {score_splt[0]}:|{amarelo_casa}|Cartões Amarelos {score_splt[-1]}:|{amarelo_fora}|Cartões Vermelhos {score_splt[0]}:|{red_casa}|Cartões Vermelhos {score_splt[-1]}:|{red_fora}|Escanteios {score_splt[0]}:|{cantos_casa}|Escanteios {score_splt[-1]}:|{cantos_fora}|Estimativa de gols {score_splt[0]}:|{expected[0]}|Estimativa de gols {score_splt[-1]}:|{expected[1]}|'''
    else:
        print("Não Coloquei expected")
        stats_p = stats_p + f'''Cartões Amarelos {score_splt[0]}:|{amarelo_casa}|Cartões Amarelos {score_splt[-1]}:|{amarelo_fora}|Cartões Vermelhos {score_splt[0]}:|{red_casa}|Cartões Vermelhos {score_splt[-1]}:|{red_fora}|Escanteios {score_splt[0]}:|{cantos_casa}|Escanteios {score_splt[-1]}:|{cantos_fora}|'''

    return score_splt, stats_p, incidents


async def alt_monit(score_splt, stats_p, fatos):
    facts = ""
    for fat in fatos:
        facts = facts + fat + "\n"
    stats_now = f'''{score_splt[-4]}|{score_splt[-2]}|{score_splt[1]}|{stats_p}Fatos do jogo'''
    # {facts}
    return stats_now


async def normal_monit(pagina, score_splt, stats_p):
    stats = ""
    sum = ""
    facts_frame = ""
    facts_normal = ""
    frame = False
    fato = ""

    await pagina.wait_for_selector(".control-button")
    control = pagina.locator(".control-button")
    for but in range(await control.count()):
        # print(await control.nth(but).inner_html())
        html = await control.nth(but).inner_html()
        if "M20 6.021V18H4V6.021h16zm-.938" in html:
            btn_state = await control.nth(but).get_attribute("class")

            if "active" not in btn_state:
                # print(but)
                await control.nth(but).click()
                print("Ativei o Botao!")
                await asyncio.sleep(3)

            break

    # btn_state = await control.nth(4).get_attribute("class")
    # if "active" not in btn_state:
    #    await control.nth(4).click()
    #    print("Ativei o Botao!")
    #    await asyncio.sleep(3)

    frames = pagina.frames
    print(f"Total de frames:{len(frames)}")

    if len(frames) > 3:
        frame = True
        wab_f = True
        while wab_f:
            await asyncio.sleep(2)
            frames = pagina.frames
            for ind, i in enumerate(frames):
                if "wab" in str(i):
                    print(
                        f"Achei o frame, vou monitorar normalmente no modo alternativo")
                    # print(i)
                    wab_f = False
                    wab = frames[ind]
                    tracker = wab.locator(".stats-tracker")
                    await tracker.locator(".icon.icon-commentary").click()
                    await asyncio.sleep(1)
                    coments = await tracker.locator(".comments.major.corner").inner_text()
                    lista_coments = coments.split("\n")

                    if await tracker.locator(".icon.icon-team-stats").is_visible():
                        await tracker.locator(".icon.icon-team-stats").click()
                        await asyncio.sleep(1)
                        cw = tracker.locator(".custom-widget")
                        for wid in range(await cw.count()):
                            # await asyncio.sleep(2)
                            sum = sum + await cw.nth(wid).inner_text() + "\n"
                            lista_sum = sum.split("\n")

                        lista_sum.insert(16, "Cartões Amarelos")
                        lista_sum.insert(19, "Cartões Vermelhos")
                        # print(f"Sumário do jogo:{lista_sum}")
                        stats = lista_sum

                    # print(f"Lances do jogo:{lista_coments}")
                    facts_frame = lista_coments
                    break

    else:

        await pagina.wait_for_selector("role=tab")
        print("Monitorando normalmente")
        l_crono = pagina.locator('role=tab')
        await l_crono.nth(1).click()
        await asyncio.sleep(3)
        await pagina.wait_for_selector(".sr-lmt-plus-1-detailed-statistics__content")
        estatisticas = await pagina.locator(
            ".sr-lmt-plus-1-detailed-statistics__content").inner_text()
        stats = estatisticas.split("\n")

        await l_crono.nth(2).click()
        await asyncio.sleep(3)
        await pagina.wait_for_selector(
            ".sr-lmt-plus-pbp-tennis-handball__row.sr-lmt-plus-pbp-event__wrapper")
        atual = pagina.locator(
            ".sr-lmt-plus-pbp-tennis-handball__row.sr-lmt-plus-pbp-event__wrapper")

        for a in range(await atual.count()):
            lst_atu = await atual.nth(a).inner_text()
            lst_atu = lst_atu.split("\n")
            if len(lst_atu) > 3:
                fato += lst_atu[0] + "\n"
                fato += lst_atu[1] + "\n"
                fato += lst_atu[2] + "\n"
                logging.info(f"Achei um score solto: \n{await atual.nth(a).inner_text()}")
            else:
                fato = fato + await atual.nth(a).inner_text() + "\n"

        fato_splt = fato.split("\n")

        for fat in fato_splt:
            facts_normal = facts_normal + fat + "\n"

    if stats:

        for i in range(len(stats)):
            if stats[i] == "OPORTUNIDADES DE GOLO":
                stats_p = stats_p + f'''Oportunidades de gol {score_splt[0]}:|{stats[i - 1]}|Oportunidades de gol {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "Remates":
                stats_p = stats_p + f'''Chutes totais {score_splt[0]}:|{stats[i - 1]}|Chutes totais {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "Remates Para Fora":
                stats_p = stats_p + f'''Chutes para fora {score_splt[0]}:|{stats[i - 1]}|Chutes para fora {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "REMATES À BALIZA" or stats[i] == "Remates À Baliza":
                if "Chutes ao gol" not in stats_p:
                    stats_p = stats_p + f'''Chutes no alvo {score_splt[0]}:|{stats[i - 1]}|Chutes no alvo {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "Precisão Nas Finalizações":
                stats_p = stats_p + f'''Precisão nas finalizações {score_splt[0]}:|{stats[i - 1]}|Precisão nas finalizações {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "POSSE DE BOLA":
                if await Lib.is_percent(stats[i - 1]):
                    stats_p = stats_p + f'''Posse de bola {score_splt[0]}:|{stats[i - 1]}|Posse de bola {score_splt[-1]}:|{stats[i + 1]}|'''
                else:
                    pass
                    # stats_p = stats_p + f'''Posse de bola {score_splt[0]}:|{stats[i - 1]}|Posse de bola {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "ATAQUE PERIGOSO" or stats[i] == "Ataques Perigosos":
                if stats[i - 1].isdigit():
                    stats_p = stats_p + f'''Ataques perigosos {score_splt[0]}:|{stats[i - 1]}|Ataques perigosos {score_splt[-1]}:|{stats[i + 1]}|'''
                else:
                    stats_p = stats_p + f'''Ataque perigoso {score_splt[0]}:|{stats[i - 1]}|Ataque perigoso {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "ATAQUE":
                stats_p = stats_p + f'''Ataque {score_splt[0]}:|{stats[i - 1]}|Ataque {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "BOLA SEGURA":
                stats_p = stats_p + f'''Bola segura {score_splt[0]}:|{stats[i - 1]}|Bola segura {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "DEFESAS":
                stats_p = stats_p + f'''Defesas {score_splt[0]}:|{stats[i - 1]}|Defesas {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "FORAS DE JOGO" or stats[i] == "Foras De Jogo":
                stats_p = stats_p + f'''Impedimentos {score_splt[0]}:|{stats[i - 1]}|Impedimentos {score_splt[-1]}:|{stats[i + 1]}|'''

            if stats[i] == "FALTAS" or stats[i] == "Faltas Cometidas":
                stats_p = stats_p + f'''Faltas {score_splt[0]}:|{stats[i - 1]}|Faltas {score_splt[-1]}:|{stats[i + 1]}|'''

    if frame:
        stats_now = f'''{score_splt[-4]}|{score_splt[-2]}|{score_splt[1]}|{stats_p}Fatos do jogo'''
        # {facts_frame}
    else:
        stats_now = f'''{score_splt[-4]}|{score_splt[-2]}|{score_splt[1]}|{stats_p}Fatos do jogo'''
    # {facts_normal}
    return stats_now


async def promise(rotina, pagina, match):
    jogo = await soloq_jogos.get()
    try:
        print(f"Ainda na soloq:{soloq_jogos.qsize()}")
        logging.info(f"Ainda na soloq:{soloq_jogos.qsize()}")
        print(f"Observador {rotina + 1} no jogo de número {jogo}!")
        Observers[rotina] = f"Observador {rotina + 1} no jogo de número {jogo}!"
        print(Observers)
        logging.info(f"lista dos observadores: {Observers}")
        logging.info(f"Observador {rotina + 1} no jogo de número {jogo}!")
        await match.nth(jogo).hover()
        await match.nth(jogo).click()
        await asyncio.sleep(1)
        await pagina.wait_for_selector(".control-events-title")
        locator = pagina.locator(".control-events-title")
        html_events = await locator.inner_html()

        if "FOOT" in html_events:
            print("Confirmei e é jogo!")
            logging.info("Confirmei e é jogo!")
        else:
            logging.error("Confirmei e não é jogo!")
            return print("Confirmei e não é jogo!")

        if "(Esports)" not in await match.nth(jogo).inner_text():
            if "(Simulação)" not in await match.nth(jogo).inner_text():
                await pagina.wait_for_selector(".scoreboard__top")
                score = await pagina.locator(".scoreboard__top").inner_text()
                score_splt = score.split("\n")
                casa = score_splt[0]
                while casa not in await match.nth(jogo).inner_text():
                    score = await pagina.locator(".scoreboard__top").inner_text()
                    score_splt = score.split("\n")
                    casa = score_splt[0]

                fora = score_splt[-1]
                tempo = score_splt[1]

                if tempo == "0:00":
                    logging.error("O jogo ainda não começou!")
                    return print("O jogo ainda não começou!")

                score_splt, stats_p, fatos_drop = await initial_monit(pagina)

                await pagina.wait_for_selector(".control-events-title")
                await pagina.locator(".control-events-title").click()
                await asyncio.sleep(1)
                await pagina.wait_for_selector(".dropdown-item")
                drop = pagina.locator(".dropdown-item")

                for d in range(await drop.count()):
                    if await drop.nth(d).inner_text() == f"{casa} - {fora}":
                        await pagina.locator(".control-events-title").click()
                        stats_now = await normal_monit(pagina, score_splt, stats_p)
                        break
                else:
                    await pagina.locator(".control-events-title").click()
                    stats_now = await alt_monit(score_splt, stats_p, fatos_drop)

                if not ativo:
                    return await trigger("Motor da função apostador interrompido pelo usuário!")

                print(f"Observador {rotina + 1} no jogo de número {jogo}, terminou sua tarefa!")
                logging.info(f"Observador {rotina + 1} no jogo de número {jogo}, terminou sua tarefa!")
                await Inter_csv.write_csv(casa, fora, stats_now)

            else:
                print("Jogo simulação, passei!")
                logging.info("Jogo simulação, passei!")

        else:
            print("Jogo Esport, passei!")
            logging.info("Jogo Esport, passei!")

    except IndexError as error:
        print(f"Deu out of range, vou continuar e tirar o item da lista: {error.__class__}")
        print(error)
        print(format_tb(error.__traceback__))
        info = f'''
Deu merda, aqui no try da soloq_jogos, erro de range: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
        print(f"Observador {rotina + 1} no jogo de número {jogo}, pulou a tarefa devido a um erro!")
        logging.error(info)

    except Exception as error:
        print(f"Deu merda, aqui o que foi: {error.__class__}")
        print(error)
        print(format_tb(error.__traceback__))
        info = f'''
Deu merda, aqui no try da soloq_jogos, o que foi: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
        logging.error(info)

    Observers[rotina] = "Stand By"
    logging.info(f"Observador {rotina + 1} terminou todas as atividades!")
    return print(f"Observador {rotina + 1} terminou todas as atividades!")


async def multi_pages(rotina):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
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
            # print(quant_jg)
            match = pagina.locator('.live-events-event-row__main')
            qtd = re.search(r"\d+", quant_jg)
            qtd = int(qtd.group())
            qtd_rows = await match.count()
            # print(qtd)
            # print(qtd_rows)
            t_final = time.time()
            if t_final - t_inicial > 120:
                print(f"Demorou tempo demais, vou fazer assim mesmo!")
                qtd_rows = qtd
        else:
            print("Farei a rotina porque igualou!")

            while not soloq_jogos.empty():

                task = promise(rotina, pagina, match)
                try:
                    await asyncio.wait_for(task, timeout=60)
                except asyncio.TimeoutError:
                    print(f"Demorou tempo demais, vou reiniciar a rotina se ainda tiverem itens na queue!")
                    logging.info("Demorou tempo demais, vou reiniciar a rotina se ainda tiverem itens na queue!")
                    await trigger("⚠️ Demorou tempo demais, vou reiniciar a rotina se ainda tiverem itens na queue!")

            await browser.close()


async def monitorar():
    async with async_playwright() as p:
        try:
            while ativo:
                browser = await p.chromium.launch(headless=True)
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
                    # print(quant_jg)
                    match = pagina.locator('.live-events-event-row__main')
                    qtd = re.search(r"\d+", quant_jg)
                    qtd = int(qtd.group())
                    qtd_rows = await match.count()
                    # print(qtd)
                    # print(qtd_rows)
                    t_final = time.time()
                    if t_final - t_inicial > 120:
                        print(f"Demorou tempo demais, vou fazer assim mesmo!")
                        qtd_rows = qtd
                else:

                    qtd_fut = pagina.locator(r"text=Futebol (")
                    qtd_fut = await qtd_fut.inner_text()
                    qtd_fut = re.search(r"\d+", qtd_fut)
                    qtd_fut = int(qtd_fut.group())
                    await browser.close()
                    await solo_queue(qtd_fut)
                    await asyncio.sleep(random.randrange(300, 600))

        except Exception as error:
            print(f"Deu merda, aqui o que foi: {error.__class__}")
            print(error)
            print(format_tb(error.__traceback__))
            logging.error(format_tb(error.__traceback__))


async def solo_queue(qtd_fut):
    list_soloq = []
    for qt in range(qtd_fut):
        list_soloq.append(qt)

    random.shuffle(list_soloq)

    for ind, item in enumerate(list_soloq):
        await soloq_jogos.put(int(list_soloq[ind]))

    if qtd_fut >= 16:
        await asyncio.gather(multi_pages(0), multi_pages(1), multi_pages(2), multi_pages(3))
    elif qtd_fut >= 9:
        await asyncio.gather(multi_pages(0), multi_pages(1), multi_pages(2))
    elif qtd_fut >= 6:
        await asyncio.gather(multi_pages(0), multi_pages(1))
    elif qtd_fut > 1:
        await asyncio.gather(multi_pages(0))
    else:
        await trigger("Não há Jogos para monitorar!")

    print("Rodada de monitoramento concluída!")
    logging.info("Rodada de monitoramento concluída!")


async def trigger(info):
    infos.append(info)
    logging.info(f"Ativei o trigger, ta ai a info:\n{info}")
    print("Adicionei uma atualização!")
