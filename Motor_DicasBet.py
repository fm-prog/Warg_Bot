from playwright.sync_api import sync_playwright
import dicas_bet


def dicas_dicasbet():
    with sync_playwright() as p:
        lista_dicasbet = []
        lst_jogos = []
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://dicasbet.com.br/palpites-de-futebol/")
        jogos = page.locator(".match").all_inner_texts()
        for i in jogos:
            lst_jogos.append(i)

        t_confrontos = len(lst_jogos)

        for i in range(t_confrontos):
            confronto = lst_jogos[i].split()
            confronto.reverse()
            an = confronto[0]
            am = confronto[1]
            over3 = confronto[2]
            over2 = confronto[3]
            over1 = confronto[4]
            ht2 = confronto[5]
            htx = confronto[6]
            ht1 = confronto[7]
            time_f = confronto[8]
            c_empate = confronto[9]
            time_c = confronto[10]
            casa = ""
            fora = ""
            del (confronto[0:11])
            confronto.reverse()

            horario = confronto[0]
            if confronto[1] == "vitória":
                palpite = confronto[1] + " " + confronto[2]
                del (confronto[0:3])
            if confronto[1] == "casa":
                palpite = confronto[1] + " " + confronto[2] + " " + confronto[3]
                del (confronto[0:4])
            if confronto[1] == "fora":
                palpite = confronto[1] + " " + confronto[2] + " " + confronto[3]
                del (confronto[0:4])
            if confronto[1] == "Empate":
                palpite = confronto[1]
                del (confronto[0:2])

            flag = 0
            for e in confronto:
                if e == "adiado":
                    horario = e
                elif flag == 1:
                    fora = fora + " " + e
                elif e == "–":
                    flag = 1
                elif flag == 0:
                    casa = casa + " " + e

            confronto.clear()
            match = dicas_bet.Dicasbet(horario, casa, fora, palpite, time_c, c_empate, time_f, ht1, htx, ht2, over1,
                                       over2,
                                       over3, am, an)
            lista_dicasbet.append(match)
        dicas = []
        for i in range(len(lista_dicasbet)):
            dicas.append(lista_dicasbet[i].mostrar())

        browser.close()

        return dicas
