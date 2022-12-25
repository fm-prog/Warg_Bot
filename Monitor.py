import asyncio
import random
from traceback import format_tb
import Torcer
from playwright.async_api import async_playwright
import time
import Warg
import logging
import Func_Lib as Lib


async def catch_alt(penal, canto, fato_splt, score_splt, stats_p, alerta, amarelo, vermelho, gol, x, y):
    lance_now = ""

    if canto:
        lance_now = f'''\n
⛳️ Escanteio!\n  
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                                                                                                                                                                                                                                                                     
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n                                                
{stats_p}'''

    elif vermelho:
        lance_now = f'''\n
🟥 Cartão Vermelho!\n                                                  
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                  
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    elif amarelo:
        lance_now = f'''\n
🟨 Cartão Amarelo!\n                                                    
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                  
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n   
{stats_p}'''

    elif penal:
        if fato_splt[y] == "Pênalti perdido":
            lance_now = f'''\n
⚠️ ⛔️🥅 Perdeu!\n                                                             
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''
        else:
            lance_now = f'''\n
⚠️ 🥅 Penal!\n                                                             
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    elif gol:
        if fato_splt[y] == "Correção: sem gol":
            lance_now = f'''\n
❌ Anulou!!\n                                                             
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''
        else:
            lance_now = f'''\n
🥅 Gol!\n                                                             
⌛️  {fato_splt[x]}\n                                                                                                     
⚠️ {fato_splt[y]}\n                                                
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    if lance_now != "":

        print(f"O alerta foi:\n{alerta}")
        logging.info(f"O alerta foi:\n{alerta}")
        print("Ativou a função catch_alt!")
        logging.info("ativou a função catch_alt!")
        await Warg.trigger(lance_now)
        penal = False
        lance = False
        gol = False
        canto = False
        amarelo = False
        vermelho = False
        alerta = ""
        # print("Unpack:", lance, gol, canto, amarelo, vermelho, alerta, penal)
        return [lance, gol, canto, amarelo, vermelho, alerta, penal]
    else:
        print(f"O alerta foi:\n{alerta}")
        logging.info(f"O alerta foi:\n{alerta}")
        print("Esse evento já foi notificado!")
        logging.info("Esse evento já foi notificado!")
        lance = False
        gol = False
        canto = False
        amarelo = False
        vermelho = False
        penal = False
        alerta = ""
        # print("Unpack:", lance, gol, canto, amarelo, vermelho, alerta, penal)
        return [lance, gol, canto, amarelo, vermelho, alerta, penal]


async def catch_normal(penal, canto, fato_splt, score_splt, stats_p, alerta, amarelo, vermelho, gol, z, y, x):
    lance_now = ""

    if canto:
        lance_now = f'''\n
⛳️ Escanteio!\n                                                                                                     
⚠️ {fato_splt[z]}\n                                                                                                    
➕ {fato_splt[y]}\n                                                                                                  
⌛️  {fato_splt[x]}\n                                                                                                
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n                                                
{stats_p}'''

    elif vermelho:
        lance_now = f'''\n
🟥 Cartão Vermelho!\n                                                  
⚠️ {fato_splt[z]}\n                                                      
➕ {fato_splt[y]}\n                                                    
⌛️  {fato_splt[x]}\n                                                  
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    elif amarelo:
        lance_now = f'''\n
🟨 Cartão Amarelo!\n                                                    
⚠️ {fato_splt[z]}\n                                                       
➕ {fato_splt[y]}\n                                                     
⌛️  {fato_splt[x]}\n                                                   
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n   
{stats_p}'''

    elif penal:
        lance_now = f'''\n
⚠️ 🥅 Penal!\n                                                             
⚠️ {fato_splt[z]}\n                                                     
➕ {fato_splt[y]}\n                                                   
⌛️ {fato_splt[x]}\n                                                 
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    elif gol:
        lance_now = f'''\n
🥅 Gol!\n                                                             
⚠️ {fato_splt[z]}\n                                                     
➕ {fato_splt[y]}\n                                                   
⌛️ {fato_splt[x]}\n                                                 
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n  
{stats_p}'''

    if lance_now != "":

        print(f"O alerta foi:\n{alerta}")
        logging.info(f"O alerta foi:\n{alerta}")
        print("Ativou a função catch_normal!")
        logging.info("ativou a função catch_normal!")
        await Warg.trigger(lance_now)
        lance = False
        gol = False
        canto = False
        amarelo = False
        vermelho = False
        penal = False
        alerta = ""
        # print("Unpack:", lance, gol, canto, amarelo, vermelho, alerta, penal)
        return [lance, gol, canto, amarelo, vermelho, alerta, penal]
    else:
        print(f"O alerta foi:\n{alerta}")
        logging.info(f"O alerta foi:\n{alerta}")
        print("Esse evento já foi notificado!")
        logging.info("Esse evento já foi notificado!")
        lance = False
        gol = False
        canto = False
        amarelo = False
        vermelho = False
        penal = False
        alerta = ""
        # print("Unpack:", lance, gol, canto, amarelo, vermelho, alerta, penal)
        return [lance, gol, canto, amarelo, vermelho, alerta, penal]


class Watcher:
    def __init__(self):
        self.observar = Torcer.Jogo()
        self.torcer_penal = Torcer.Observer_Penal()
        self.torcer_red = Torcer.Observer_Red_Card()
        self.torcer_yellow = Torcer.Observer_Yellow_Card()
        self.torcer_cantos = Torcer.Observer_cantos()
        self.torcer_gol = Torcer.Observer_gol()
        self.torcer_warg = Torcer.Observer_warg()

    async def monitorar(self, link, alternativo, ind_obs, low_mem):
        await self.observar.assistir(self.torcer_penal)
        await self.observar.assistir(self.torcer_yellow)
        await self.observar.assistir(self.torcer_red)
        await self.observar.assistir(self.torcer_cantos)
        await self.observar.assistir(self.torcer_gol)
        await self.observar.assistir(self.torcer_warg)
        stats_p = ""
        fato = ""
        tamanho_ant = 0
        observ = 1
        try_again = 0
        x = 0
        y = 1
        z = 2
        alt_monit = alternativo
        t_obs = 0
        time_space = random.randrange(15, 30)
        st = False
        sum = ""
        stats = ""

        async with async_playwright() as p:

            monitor = Watcher()

            if low_mem:
                alt_monit = True

            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            pagina = await context.new_page()
            response = await pagina.goto("https://br.betano.com" + link, timeout=0)
            try:
                if response.request.redirected_from.redirected_to:
                    info = f'''<b>O link do jogo que eu estava acompanhando: https://br.betano.com{link}, sumiu!\n
            O jogo deve ter acabado!</b>'''
                    logging.info(info)
                    await self.observar.sair(self.torcer_yellow)
                    await self.observar.sair(self.torcer_red)
                    await self.observar.sair(self.torcer_cantos)
                    await self.observar.sair(self.torcer_gol)
                    await self.observar.sair(self.torcer_warg)
                    await self.observar.sair(self.torcer_penal)
                    await context.close()
                    await browser.close()
                    Warg.monitorados[ind_obs] = "Stand By"
                    del (Warg.paginas[Warg.paginas.index(link)])
                    await Warg.trigger(info)
                    return print("A Url não é válida")

            except Exception as error:
                print(error)
                print("Verifiquei e a Url é válida!")

                if pagina.expect_popup():
                    await pagina.keyboard.press("Escape")

                if alt_monit:
                    await pagina.wait_for_selector(".live-incidents__container__title")
                    drop = pagina.locator(".live-incidents__container__title")
                    await drop.click()

                timeout = False
                while not timeout:
                    await context.tracing.start(screenshots=True, snapshots=True)

                    if Warg.monitorados[ind_obs] == "Close":
                        info = f"<b>✅ O observador {ind_obs + 1} deixou de acompanhar o jogo:\n https://br.betano.com{link}</b>"
                        await Warg.trigger(info)
                        logging.info(info)
                        await self.observar.sair(self.torcer_yellow)
                        await self.observar.sair(self.torcer_red)
                        await self.observar.sair(self.torcer_cantos)
                        await self.observar.sair(self.torcer_gol)
                        await self.observar.sair(self.torcer_warg)
                        await self.observar.sair(self.torcer_penal)
                        await context.close()
                        await browser.close()
                        Warg.monitorados[ind_obs] = "Stand By"
                        del (Warg.paginas[Warg.paginas.index(link)])
                        return print("Encerrei o monitoramento")

                    red_casa = 0
                    amarelo_casa = 0
                    red_fora = 0
                    amarelo_fora = 0
                    cantos_casa = 0
                    cantos_fora = 0

                    t_inicial = time.time()

                    try:
                        await pagina.wait_for_selector(".scoreboard__top")
                        score = await pagina.locator(".scoreboard__top").inner_text()
                        score_splt = score.split("\n")

                        if not alt_monit:
                            await pagina.wait_for_selector(".live-incidents__container__title")
                            drop = pagina.locator(".live-incidents__container__title")
                            await drop.click()

                        await pagina.wait_for_selector(".sb-dropdown--extended")
                        incidents = await pagina.locator(".sb-dropdown--extended").inner_text()
                        incidents = incidents.split("\n")

                        for ind, inc in enumerate(incidents):
                            if await Lib.is_tempo(inc):
                                incidents[ind] = incidents[ind].replace("'", "")

                        print(f"Incidents bruto:\n{incidents}")

                        # Monitoramento normal
                        if not alt_monit:
                            await pagina.wait_for_selector(".control-button")
                            control = pagina.locator(".control-button")
                            #print(await control.nth(4).inner_html())
                            #print(await control.nth(3).inner_html())
                            #print(await control.nth(2).inner_html())
                            #print(await control.nth(1).get_attribute("name"))
                            btn_state = await control.nth(4).get_attribute("class")
                            if "active" not in btn_state:
                                await control.nth(4).click()
                                print("Ativei o Botao!")
                                await asyncio.sleep(3)

                            frames = pagina.frames
                            print(f"Total de frames:{len(frames)}")

                            if len(frames) > 3:
                                wab_f = True
                                while wab_f:
                                    await asyncio.sleep(2)
                                    frames = pagina.frames
                                    for ind, i in enumerate(frames):
                                        if "wab" in str(i):
                                            print(
                                                f"Achei o frame, vou monitorar normalmente no modo alternativo: {link}")
                                            print(i)
                                            wab_f = False
                                            wab = frames[ind]
                                            tracker = wab.locator(".stats-tracker")
                                            await tracker.locator(".icon.icon-commentary").click()
                                            coments = await tracker.locator(".comments.major.corner").inner_text()
                                            lista_coments = coments.split("\n")

                                            if await tracker.locator(".icon.icon-team-stats").is_visible():
                                                await tracker.locator(".icon.icon-team-stats").click()
                                                cw = tracker.locator(".custom-widget")
                                                for wid in range(await cw.count()):
                                                    # await asyncio.sleep(2)
                                                    sum = sum + await cw.nth(wid).inner_text() + "\n"
                                                    lista_sum = sum.split("\n")

                                                lista_sum.insert(16, "Cartões Amarelos")
                                                lista_sum.insert(19, "Cartões Vermelhos")
                                                print(f"Sumário do jogo:{lista_sum}")
                                                stats = lista_sum

                                            print(f"Lances do jogo:{lista_coments}")
                                            tamanho_atu = len(lista_coments)
                                            fato_splt = lista_coments
                                            await control.nth(4).click()
                                            break

                            else:

                                try:
                                    await pagina.wait_for_selector("role=tab")
                                except TimeoutError:
                                    await control.nth(4).click()
                                    await pagina.wait_for_selector("role=tab")
                                print("Monitorando normalmente: ", link)
                                logging.info(f"Monitorando normalmente: {link}")
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
                                tamanho_atu = await atual.count()

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

                        # Monitoramento alternativo
                        else:
                            print("Monitoramento alternativo: ", link)
                            logging.info(f"Monitoramento alternativo:  {link}")
                            fato_splt = incidents

                            for ind, inc in enumerate(fato_splt):

                                if inc == "Pênalti perdido" and not fato_splt[ind - 1].isdigit():
                                    fato_splt.insert(ind, fato_splt[ind + 1])

                                if inc == score_splt[0]:
                                    # inc_find = re.search("[a-z]", fato_splt[ind - 1])
                                    # if not inc_find:
                                    fato_splt[ind] = f"Gol! - {score_splt[0]}"

                                if inc == score_splt[-1]:
                                    # inc_find = re.search("[a-z]", fato_splt[ind - 1])
                                    # if not inc_find:
                                    fato_splt[ind] = f"Gol! - {score_splt[-1]}"
                            # await drop.click()

                            print(f"Transformei os incidents, receba!\n{fato_splt}")

                            tamanho_atu = len(fato_splt)

                        print(f"Tamanho atual: {tamanho_atu}")
                        print(f"Tamanho anterior: {tamanho_ant}")
                        logging.info(f"Tamanho atual: {tamanho_atu}")
                        logging.info(f"Tamanho anterior: {tamanho_ant}")

                        if tamanho_atu > tamanho_ant or tamanho_ant > tamanho_atu or tamanho_ant == tamanho_atu:

                            diff = abs(tamanho_ant - tamanho_atu)

                            print(f"Mid diff: {diff}")
                            logging.info(f"Mid diff: {diff}")

                            # For para pegar o status do jogo
                            for i, inc in enumerate(incidents):

                                if "prorrogação" in inc:
                                    print("A prorrogação ta rolando tá rolando...")
                                    logging.info(f"A prorrogação ta rolando tá rolando...")
                                    break

                                if inc == "Início do segundo tempo":
                                    print("O segundo tempo tá rolando...")
                                    st = True
                                    logging.info(f"O segundo tempo tá rolando...")
                                    break

                                if inc == "Fim do primeiro tempo":
                                    print(
                                        f"Oque,quando,quem: {incidents[i]} - 45+ - ⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}")
                                    quem = f"{score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}"
                                    await self.observar.atualizacao(incidents[i], "999", quem)
                                    print("Final do primeiro tempo!")
                                    logging.info(f"{incidents[i]} - 45+ - {quem}")
                                    logging.info(f"Final do primeiro tempo!")
                                    break

                                if inc == "Fim do segundo tempo" or inc == "Fim da partida":
                                    print(
                                        f"Oque,quando,quem: {incidents[i]} - 90+ - ⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}")
                                    quem = f"{score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}"
                                    await self.observar.atualizacao(incidents[i], "999", quem)
                                    print("Final do jogo!")
                                    logging.info(f"{incidents[i]} - 90+ - {quem}")
                                    logging.info(f"Final do jogo!")
                                    break

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

                            stats_p = stats_p + f'''
🟨 Cartões Amarelos:\n
{score_splt[0]} - {amarelo_casa}
{score_splt[-1]} - {amarelo_fora}\n
🟥 Cartões Vermelhos:\n
{score_splt[0]} - {red_casa}
{score_splt[-1]} - {red_fora}\n
⛳️ Escanteios:\n                                                             
{score_splt[0]} - {cantos_casa}                                             
{score_splt[-1]} - {cantos_fora}\n'''

                            if not alt_monit:
                                if stats:

                                    for i in range(len(stats)):
                                        if stats[i] == "OPORTUNIDADES DE GOLO":
                                            stats_p = stats_p + f'''
❌🥅 Oportunidades de gol:\n
{score_splt[0]} - {stats[i - 1]} 
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "Remates":
                                            stats_p = stats_p + f'''
👟 Chutes totais:\n
{score_splt[0]} - {stats[i - 1]} 
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "Remates Para Fora":
                                            stats_p = stats_p + f'''
👟❌🥅 Chutes para fora:\n
{score_splt[0]} - {stats[i - 1]} 
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "REMATES À BALIZA" or stats[i] == "Remates À Baliza":
                                            if "Chutes ao gol" not in stats_p:
                                                stats_p = stats_p + f'''
👟 🥅 Chutes ao gol:\n                                                         
{score_splt[0]} - {stats[i - 1]}                                             
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "Precisão Nas Finalizações":
                                            stats_p = stats_p + f'''
👟🎯🥅 Precisão nas finalizações:\n
{score_splt[0]} - {stats[i - 1]}% 
{score_splt[-1]} - {stats[i + 1]}%\n'''

                                        if stats[i] == "POSSE DE BOLA":
                                            if stats[i - 1].isdigit() and stats[i + 1].isdigit():
                                                stats_p = stats_p + f'''
⚽️ Posse de Bola:\n                                                                 
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''
                                            else:
                                                stats_p = stats_p + f'''
⚽️ Posse de Bola:\n                                                                 
{score_splt[0]} - {stats[i - 2]}%                                                    
{score_splt[-1]} - {stats[i + 2]}%\n'''

                                        if stats[i] == "ATAQUE PERIGOSO" or stats[i] == "Ataques Perigosos":
                                            if stats[i - 1].isdigit():
                                                stats_p = stats_p + f'''
🎯 Ataques Perigosos:\n                                                               
{score_splt[0]} - {stats[i - 1]}                                                   
{score_splt[-1]} - {stats[i + 1]}\n'''
                                            else:
                                                stats_p = stats_p + f'''
🎯 Ataque Perigoso:\n                                                               
{score_splt[0]} - {stats[i - 1]}                                                   
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "ATAQUE":
                                            stats_p = stats_p + f'''
🎯 Ataque:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "BOLA SEGURA":
                                            stats_p = stats_p + f'''
⚽️ Bola Segura:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "DEFESAS":
                                            stats_p = stats_p + f'''
🥅🎯 Defesas:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "FORAS DE JOGO" or stats[i] == "Foras De Jogo":
                                            stats_p = stats_p + f'''
⛔️⚽️ Impedimentos:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''

                                        if stats[i] == "FALTAS" or stats[i] == "Faltas Cometidas":
                                            stats_p = stats_p + f'''
✖️⚽️ Faltas:\n                                                                         
{score_splt[0]} - {stats[i - 1]}                                                    
{score_splt[-1]} - {stats[i + 1]}\n'''

                            print(f"Fatos do jogo:\n {fato_splt}")
                            # print(f"Stats do jogo:\n {stats_p}")
                            print(f"Fatos do drop:\n {incidents}")

                            if self.observar.lance:

                                if self.observar.end:
                                    lance_now = f'''\n
⚠️Acabou!\n                                                                                                       
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n
{stats_p}
⚠️ #Partiu, os observadores terminaram o trabalho e estão a espera de uma nova tarefa!\n'''
                                    await self.observar.sair(self.torcer_yellow)
                                    await self.observar.sair(self.torcer_red)
                                    await self.observar.sair(self.torcer_cantos)
                                    await self.observar.sair(self.torcer_gol)
                                    await self.observar.sair(self.torcer_warg)
                                    await self.observar.sair(self.torcer_penal)
                                    await context.close()
                                    await browser.close()
                                    Warg.monitorados[ind_obs] = "Stand By"
                                    del (Warg.paginas[Warg.paginas.index(link)])
                                    await Warg.trigger(lance_now)
                                    logging.info(f"O jogo acabou! {lance_now}")
                                    return print("O jogo acabou!")

                                if self.observar.half:
                                    lance_now = f'''\n
⚠️ Intervalo!\n                                                                                                   
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n
{stats_p}
⚠️ #Partiu, os observadores foram tomar uma gelada, voltarão quando o intervalo acabar!\n'''
                                    Warg.monitorados[ind_obs] = lance_now
                                    logging.info(f"O jogo tá no intervalo! {lance_now}")
                                    asyncio.create_task(monitor.intervalo(link, alternativo, ind_obs, low_mem))
                                    print("Vou iniciar a corotina do intervalo!")
                                    logging.info("Vou iniciar a corotina do intervalo!")
                                    await context.close()
                                    await browser.close()
                                    return await Warg.trigger(lance_now)

                            if len(fato_splt) > 2 and (
                                    ("segundo tempo" not in fato_splt[0]) or ("segunda parte" not in fato_splt[0])):

                                # Atualizacao no modo alternativo
                                if alt_monit or len(frames) > 3:
                                    if diff >= 2 and tamanho_ant > 0:
                                        rows = diff
                                        x = diff - 2
                                        y = x + 1
                                        while rows >= 2:
                                            if fato_splt[y] == "Início do segundo tempo" or fato_splt[y] == "Fim do " \
                                                                                                            "primeiro " \
                                                                                                            "tempo":
                                                logging.info(
                                                    f"Peguei e descartei info da transicao de  tempo!")
                                                print(
                                                    f"Peguei e descartei info da transicao de  tempo!")
                                            else:
                                                logging.info(
                                                    f"Peguei o mid diff alternativo na {rows / 2} vez!!\nOque,quando,quem: {fato_splt[y]} - {fato_splt[x]} - Alternativo")
                                                print(
                                                    f"Peguei o mid diff alternativo na {rows / 2} vez!!\nOque,quando,quem: {fato_splt[y]} - {fato_splt[x]} - Alternativo")
                                                await self.observar.atualizacao(fato_splt[y], fato_splt[x],
                                                                                "Alternativo")

                                                if self.observar.lance:
                                                    logging.info("Deu o trigger no lance!")
                                                    lst_alt = await catch_alt(self.observar.penal, self.observar.canto,
                                                                              fato_splt,
                                                                              score_splt,
                                                                              stats_p,
                                                                              self.observar.alerta,
                                                                              self.observar.amarelo,
                                                                              self.observar.vermelho, self.observar.gol,
                                                                              x, y)
                                                    self.observar.lance = lst_alt[0]
                                                    self.observar.gol = lst_alt[1]
                                                    self.observar.canto = lst_alt[2]
                                                    self.observar.amarelo = lst_alt[3]
                                                    self.observar.vermelho = lst_alt[4]
                                                    self.observar.alerta = lst_alt[5]
                                                    self.observar.penal = lst_alt[6]

                                            x = x - 2
                                            y = y - 2
                                            rows -= 2

                                else:
                                    if diff >= 1 and tamanho_ant > 0:
                                        rows = diff
                                        if diff > 1:
                                            x = (x + 3) * (diff - 1)
                                            y = x + 1
                                            z = x + 2
                                            # print(f"Oque,quando,quem de teste: {z} - {x} - {y}")
                                        while rows >= 1:
                                            logging.info(
                                                f"Peguei o mid diff na {rows} vez!!\nOque,quando,quem: {fato_splt[z]} - {fato_splt[x]} - {fato_splt[y]}")
                                            print(
                                                f"Oque,quando,quem: {fato_splt[z]} - {fato_splt[x]} - {fato_splt[y]}")
                                            await self.observar.atualizacao(fato_splt[z], fato_splt[x], fato_splt[y])

                                            if self.observar.lance:
                                                logging.info("Deu o trigger no lance!")
                                                lst_normal = await catch_normal(self.observar.penal,
                                                                                self.observar.canto,
                                                                                fato_splt,
                                                                                score_splt,
                                                                                stats_p, self.observar.alerta,
                                                                                self.observar.amarelo,
                                                                                self.observar.vermelho,
                                                                                self.observar.gol, z,
                                                                                y, x)
                                                self.observar.lance = lst_normal[0]
                                                self.observar.gol = lst_normal[1]
                                                self.observar.canto = lst_normal[2]
                                                self.observar.amarelo = lst_normal[3]
                                                self.observar.vermelho = lst_normal[4]
                                                self.observar.alerta = lst_normal[5]
                                                self.observar.penal = lst_normal[6]

                                            x = x - 3
                                            y = y - 3
                                            z = z - 3
                                            rows -= 1

                        if len(frames) > 3:
                            if len(fato_splt) > 1 and fato_splt[0] != "Início do segundo tempo":
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n                                                                      
⚠️ Último Lance:\n                                                             
⌛️  {fato_splt[0]}\n                                                                                                     
⚠️ {fato_splt[1]}\n   
'''
                            else:
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n  
⚠️ Último Lance:\n
➕ {fato_splt[0]}\n  
'''
                        elif alt_monit:

                            if len(fato_splt) > 1 and fato_splt[0] != "Início do segundo tempo":
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n                                                                      
⚠️ Último Lance:\n                                                             
⌛️  {fato_splt[0]}\n                                                                                                     
⚠️ {fato_splt[1]}\n   
⚠️ Cobertura da Partida Limitada!\n
'''
                            else:
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n  
⚠️ Último Lance:\n
➕ {fato_splt[0]}\n  
⚠️ Cobertura da Partida Limitada!\n   
'''
                            if low_mem:
                                stats_now += "⚠️ Modo de economia de memória!\n</b>"
                            else:
                                stats_now += "</b>"

                        else:
                            if len(fato_splt) > 2 and "segundo tempo" not in incidents[0]:
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n                                                                      
⚠️ Último Lance:\n                                                             
{fato_splt[2]}\n   
⌛️ {fato_splt[0]}\n   
➕ {fato_splt[1]}\n 
'''
                            else:
                                stats_now = f'''\n
⚽️ {score_splt[0]} {score_splt[-4]} x {score_splt[-2]} {score_splt[-1]}\n       
⌛️ {score_splt[1]}\n                                                         
{stats_p}\n                                                                      
⚠️ Último Lance:\n
➕ {incidents[0]}\n     
'''

                        if observ == 1:
                            await Warg.trigger(stats_now)

                        tamanho_ant = tamanho_atu

                        if Warg.monitorados[ind_obs] != "Close":
                            Warg.monitorados[ind_obs] = stats_now

                        self.observar.alerta = ""
                        self.observar.lance = False
                        self.observar.gol = False
                        self.observar.canto = False
                        self.observar.amarelo = False
                        self.observar.vermelho = False
                        self.observar.penal = False
                        self.observar.half = False
                        stats_p = ""
                        fato = ""
                        sum = ""
                        incidents.clear()
                        if not alt_monit and stats != "":
                            stats.clear()
                        fato_splt.clear()
                        x = 0
                        y = 1
                        z = 2

                    except Exception as error:
                        print(f"Deu merda, aqui o que foi: {error.__class__}")
                        print(error)
                        print(format_tb(error.__traceback__))
                        info = f'''
Deu merda, aqui no Tryzão, o que foi: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
                        logging.error(info)
                        try_again += 1
                        info = f"Algum erro durante a execução, vou tentar de novo! Tentativas : {try_again}"
                        tamanho_ant = 0
                        tamanho_atu = 0
                        print(info)
                        logging.error(info)
                        if try_again >= 8:
                            if alt_monit:
                                info = f"<b>https://br.betano.com{link}\nNúmero de tentativas de monitoramento esgotadas!\nFiz tudo ao meu alcance!</b>"
                                await self.observar.sair(self.torcer_yellow)
                                await self.observar.sair(self.torcer_red)
                                await self.observar.sair(self.torcer_cantos)
                                await self.observar.sair(self.torcer_gol)
                                await self.observar.sair(self.torcer_warg)
                                await self.observar.sair(self.torcer_penal)
                                await context.close()
                                await browser.close()
                                Warg.monitorados[ind_obs] = "Stand By"
                                del (Warg.paginas[Warg.paginas.index(link)])
                                logging.error(info)
                                await context.tracing.stop(path="trace_error_monit.zip")
                                await Warg.trigger(info)
                                return print(
                                    f"<b>https://br.betano.com{link}\nNúmero de tentativas de monitoramento esgotadas!\nFiz tudo ao meu alcance!\nPor favor, tente torcer Nome do Time novamente!</b>")

                        if try_again == 4:
                            info = f"<b>https://br.betano.com{link}\nNúmero de tentativas de monitoramento " \
                                   f"esgotadas!\nVou tentar monitorar de outra forma!</b> "

                            response = await pagina.goto("https://br.betano.com" + link, timeout=0)
                            try:
                                if response.request.redirected_from.redirected_to:
                                    info = f'''<b>O link do jogo que eu estava acompanhando: https://br.betano.com{link}, sumiu!\n
O jogo deve ter acabado!</b>'''
                                    logging.info(info)
                                    await self.observar.sair(self.torcer_yellow)
                                    await self.observar.sair(self.torcer_red)
                                    await self.observar.sair(self.torcer_cantos)
                                    await self.observar.sair(self.torcer_gol)
                                    await self.observar.sair(self.torcer_warg)
                                    await self.observar.sair(self.torcer_penal)
                                    await context.close()
                                    await browser.close()
                                    Warg.monitorados[ind_obs] = "Stand By"
                                    del (Warg.paginas[Warg.paginas.index(link)])
                                    await Warg.trigger(info)
                                    return print("A Url não é válida")
                            except Exception as error:
                                print(error)
                                print("A Url é válida")
                                alt_monit = True
                                await Warg.trigger(info)
                                logging.error(info)
                                await context.tracing.stop(path="trace_error_monit.zip")

                    else:
                        print("Deu tudo certo!")
                        logging.info("Deu tudo certo!")
                        try_again = 0
                        await context.tracing.stop(path="trace_done_monit.zip")
                        t_final = time.time()
                        print(f"Número de Observações: {observ}")
                        logging.info(f"Número de Observações: {observ}")
                        observ += 1
                        print(f"Demorei {t_final - t_inicial} para observar!")
                        t_obs += (t_final - t_inicial)
                        print(f"Tempo decorrido: {t_obs}")
                        logging.info(f"Tempo decorrido: {t_obs}")
                        logging.info(f"Demorei {t_final - t_inicial} para observar!")

                        t_split = score_splt[1]
                        t_split = t_split.split(":")
                        score_splt.clear()

                        # print(f"O valor da variavel t_split: {t_split[0]}")

                        if int(t_split[0]) > 90 or (int(t_split[0]) > 45 and not st):
                            print("Vou aumentar a frequência das observações!")
                            logging.info("Vou aumentar a frequência das observações!")
                            time_space = 5
                            await asyncio.sleep(time_space)
                        else:
                            print("Frequência normal de observação!")
                            logging.info("Frequência normal de observação!")
                            await asyncio.sleep(time_space)

                        if t_obs > 900 and (int(t_split[0]) < 90 or int(t_split[0]) < 45):
                            await browser.close()
                            await context.close()
                            asyncio.create_task(monitor.monitorar(link, alternativo, ind_obs, low_mem))
                            logging.info("Tempo máximo de observação alcançado!")
                            return "Tempo máximo de observação alcançado!"

    @staticmethod
    async def intervalo(link, alt_monit, ind_obs, low_mem):
        async with async_playwright() as p:
            monitor = Watcher()
            try_again = 0
            status = "Fim do primeiro tempo"

            try:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                pagina = await context.new_page()
                response = await pagina.goto("https://br.betano.com" + link, timeout=0)
                try:
                    if response.request.redirected_from.redirected_to:
                        print("Verifiquei, e a Url não válida!")

                except Exception as error:
                    print(error)
                    print("Verifiquei, e a Url é válida!")
                    try:
                        if pagina.expect_popup():
                            await pagina.keyboard.press("Escape")
                    except Exception as error:
                        print(error)
                        print("Time out exception!")
                print(f"Monitorando o intervalo: {link}")
                logging.info(f"Monitorando o intervalo: {link}")
                await pagina.wait_for_selector(".live-incidents__container__title")
                drop = pagina.locator(".live-incidents__container__title")
                await drop.click()
                await pagina.wait_for_selector(".sb-dropdown--extended")

                while status == "Fim do primeiro tempo":

                    if Warg.monitorados[ind_obs] == "Close":
                        info = f"<b>✅ O observador {ind_obs + 1} deixou de acompanhar o jogo:\n https://br.betano.com{link}</b>"
                        await Warg.trigger(info)
                        logging.info(info)
                        await context.close()
                        await browser.close()
                        Warg.monitorados[ind_obs] = "Stand By"
                        del (Warg.paginas[Warg.paginas.index(link)])
                        return print("Encerrei o monitoramento")

                    incidents = await pagina.locator(".sb-dropdown--extended").inner_text()
                    incidents = incidents.split("\n")
                    for i in incidents:
                        if i == "Início do segundo tempo":
                            print("O jogo recomeçou!")
                            logging.info("O jogo recomeçou!")

                            asyncio.create_task(monitor.monitorar(link, alt_monit, ind_obs, low_mem))
                            await context.close()
                            await browser.close()
                            await Warg.trigger("<b>👁‍🗨 O segundo tempo começou!</b>")
                            return "O jogo recomeçou!"
                    await asyncio.sleep(random.randrange(30, 120))

            except Exception as error:
                print(f"Deu merda, aqui o que foi: {error.__class__}")
                print(error)
                print(format_tb(error.__traceback__))
                info = f'''
Deu merda, aqui no Tryzão, o que foi: {error.__class__}\n
{error}\n
{format_tb(error.__traceback__)}\n
'''
                logging.error(info)
                try_again += 1
                info = f"Algum erro durante a execução do Monitoramento do intervalo, vou tentar de novo! Tentativas : {try_again} "
                print(info)
                logging.error(info)
                if try_again >= 4:
                    info = f"<b>https://br.betano.com{link}\nNúmero de tentativas de monitoramento do intervalo " \
                           f"esgotadas!\nFiz tudo ao meu alcance!\nPor favor, informe: torcer Nome do time novamente " \
                           f"para mais tentativas!</b> "
                    await context.close()
                    await browser.close()
                    Warg.monitorados[ind_obs] = "Stand By"
                    del (Warg.paginas[Warg.paginas.index(link)])
                    logging.error(info)
                    return Warg.trigger(info)
