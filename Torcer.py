from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import logging
import Func_Lib as Lib

logging.basicConfig(level=logging.INFO, filename="Bot.log", format="%(asctime)s - %(levelname)s - %(message)s")


class Jogo_BP(ABC):

    @abstractmethod
    async def assistir(self, observer: Observer) -> None:
        pass

    @abstractmethod
    async def sair(self, observer: Observer) -> None:
        pass

    @abstractmethod
    async def notificar(self) -> None:
        pass


class Jogo(Jogo_BP):

    def __init__(self):
        self.alerta = ""
        self.lance = False
        self.canto = False
        self.amarelo = False
        self.vermelho = False
        self.gol = False
        self.half = False
        self.lista_facts = []
        self.end = False
        self.penal = False
        self.torcedores: List[Observer] = []

    async def assistir(self, observer: Observer) -> None:
        print(f"\n{observer} está em Stand By!")
        logging.info(f"\n{observer} está em Stand By!")
        self.torcedores.append(observer)

    async def sair(self, observer: Observer) -> None:
        print("\nUm torcedor desistiu de assistir o jogo!")
        logging.info("\nUm torcedor desistiu de assistir o jogo!")
        self.torcedores.remove(observer)

    async def atualizacao(self, oque, quando, quem):
        print(f"Fatos já notificados: {self.lista_facts}")
        logging.info(f"Fatos já notificados: {self.lista_facts}")
        print("\nNovo lance!")
        logging.info("\nNovo lance!")
        print("\nVerificando lance!")
        logging.info("\nVerificando lance!")

        if self.lista_facts:
            for i in range(len(self.lista_facts)):

                if self.lista_facts[i] == oque + "\n" + quando + "\n" + quem:
                    print("Esse evento já foi notificado!")
                    logging.info("Esse evento já foi notificado!")
                    break

                if i == len(self.lista_facts) - 1:
                    lst = self.lista_facts[i].split("\n")
                    edt_q = quando
                    lst[1] = lst[1].replace("'", "")
                    edt_q = edt_q.replace("'", "")
                    if "+" in lst[1]:
                        str_lst = lst[1].split("+")
                        int_lst = int(str_lst[0]) + int(str_lst[1])
                    else:
                        int_lst = int(lst[1])

                    if "+" in edt_q:
                        edt_q = edt_q.split("+")
                        int_edt = int(edt_q[0]) + int(edt_q[1])
                    else:
                        int_edt = int(edt_q)

                    if int_lst > int_edt:
                        print("Esse evento aconteceu antes do último já notificado!")
                        logging.info("Esse evento aconteceu antes do último já notificado!")
                        print(f"Tempo do fato notificado {int_edt} < {int_lst} do que o já listado!")
                        logging.info(f"Tempo do fato notificado {int_edt} < {int_lst} do que o já listado!")
                        break
                    else:
                        print(f"Tempo do fato notificado {int_edt} >= {int_lst} do que o já listado!")
                        logging.info(f"Tempo do fato notificado {int_edt} >= {int_lst} do que o já listado!")

                        if oque == "Fim do primeiro tempo":
                            self.alerta = oque + "\n" + "45" + "\n" + quem
                            logging.info(oque + "\n" + "45" + "\n" + quem)
                        else:
                            self.alerta = oque + "\n" + quando + "\n" + quem
                            logging.info(oque + "\n" + quando + "\n" + quem)

                        await self.notificar()
                        print("Evento notificado com êxito!")
                        logging.info("Evento notificado com êxito!")
                        break

        else:
            logging.info(oque + "\n" + quando + "\n" + quem)

            if oque == "Fim do primeiro tempo":
                self.alerta = oque + "\n" + "45" + "\n" + quem
                logging.info(oque + "\n" + "45" + "\n" + quem)
            else:
                self.alerta = oque + "\n" + quando + "\n" + quem
                logging.info(oque + "\n" + quando + "\n" + quem)

            await self.notificar()
            print("Evento notificado com êxito!")
            logging.info("Evento notificado com êxito!")

    async def notificar(self) -> None:
        print(f"\n{self.torcedores} viram o lance!")
        logging.info(f"\n{self.torcedores} viram o lance!")
        for observer in self.torcedores:
            await observer.update(self)


class Observer(ABC):

    @abstractmethod
    async def update(self, jogo: Jogo) -> None:
        pass


class Observer_Red_Card(Observer):
    async def update(self, jogo: Jogo) -> None:
        alertas = ["vermelho", "acumulação de cartões amarelos"]
        red = await Lib.match(jogo.alerta.lower(), alertas)
        if red:
            jogo.lance = True
            jogo.vermelho = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nEu vi um cartao vermelho!")
            print("\nEu vi um cartao vermelho!")


class Observer_Penal(Observer):
    async def update(self, jogo: Jogo) -> None:
        alertas = ["penalidades", "pênalti", "penalidade"]
        penal = await Lib.match(jogo.alerta.lower(), alertas)
        if penal:
            jogo.lance = True
            jogo.penal = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nEu vi um pênalti!")
            print("\nEu vi um pênalti!")


class Observer_warg(Observer):
    async def update(self, jogo: Jogo) -> None:
        if "Fim do primeiro tempo" in jogo.alerta or "Esgotaram-se os primeiros 45 minutos do encontro." in jogo.alerta:
            jogo.lance = True
            jogo.half = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nIntervalo do jogo!")
            print("\nIntervalo do jogo!")
        if "Fim do segundo tempo" in jogo.alerta or "Fim da partida" in jogo.alerta:
            jogo.lance = True
            jogo.end = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nO jogo acabou!")
            print("\nO jogo acabou!")


class Observer_Yellow_Card(Observer):
    async def update(self, jogo: Jogo) -> None:
        alertas = ["amarelo"]
        amarelo = await Lib.match(jogo.alerta.lower(), alertas)
        if amarelo:
            jogo.lance = True
            jogo.amarelo = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nEu vi um cartao amarelo!")
            print("\nEu vi um cartao amarelo!")


class Observer_gol(Observer):
    async def update(self, jogo: Jogo) -> None:
        alertas = ["golo", "converte", "marcador", "marca", "gol", "com chute", "com pênalti", "com cabeceio", "com livre"]
        gol = await Lib.match(jogo.alerta.lower(), alertas)
        if gol:
            alertas = ["não resulta", "não resultou", "perto", "fora", "mas", "fora de jogo"]
            verificar = await Lib.match(jogo.alerta.lower(), alertas)
            if verificar:
                print("Alarme falso de gol")
                logging.info("Alarme falso de gol!")
                pass
            else:
                jogo.lance = True
                jogo.gol = True
                jogo.lista_facts.append(jogo.alerta)
                logging.info("Gol!")
                print("\nGol!")
        else:
            if await Lib.is_placar(jogo.alerta):
                jogo.lance = True
                jogo.gol = True
                jogo.lista_facts.append(jogo.alerta)
                logging.info("Gol!")
                print("\nGol!")


class Observer_cantos(Observer):
    async def update(self, jogo: Jogo) -> None:
        alertas = ["canto", "escanteio"]
        canto = await Lib.match(jogo.alerta.lower(), alertas)
        if canto:
            jogo.lance = True
            jogo.canto = True
            jogo.lista_facts.append(jogo.alerta)
            logging.info("\nEscanteio!")
            print("\nEscanteio!")
