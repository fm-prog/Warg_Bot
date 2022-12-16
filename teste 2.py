import asyncio
import re
import time

from playwright.async_api import async_playwright


async def is_placar(string):
    reg_exp = r"\d+"
    return re.match(reg_exp, string)


async def normal_monit(pagina):
    fato = ""
    await pagina.wait_for_selector(".live-incidents__container__title")
    drop = pagina.locator(".live-incidents__container__title")
    await drop.click()
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
        else:
            fato = fato + await atual.nth(a).inner_text() + "\n"

    fato_splt = fato.split("\n")


async def monitorar():
    async with async_playwright() as p:
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
                            print("confirmei e é jogo")
                        else:
                            break

                        if tempo == "0:00":
                            print("O jogo ainda não começou!")
                            continue

                        await pagina.wait_for_selector(".control-events-title")
                        event = await pagina.locator(".control-events-title").inner_text()

                        if f"{casa} - {fora}" == event:
                            print("Vou monitorar de forma normal")
                            #await normal_monit(pagina)

                        else:
                            print("Vou monitorar de forma alternativa")

                        print(score_splt)
                        texto = texto + await match.nth(i).inner_text() + "\n" + "fim_jogo" + "\n"
                        print(texto)

            # jogos_live = texto.split("fim_jogo")
            # del(jogos_live[len(jogos_live) - 1])
            # print(jogos_live)


async def main():
    await asyncio.gather(monitorar())


if __name__ == '__main__':
    asyncio.run(main())
