import asyncio

import Torcer







async def main():
    observar = Torcer.Jogo()
    torcer_penal = Torcer.Observer_Penal()
    torcer_red = Torcer.Observer_Red_Card()
    torcer_yellow = Torcer.Observer_Yellow_Card()
    torcer_cantos = Torcer.Observer_cantos()
    torcer_gol = Torcer.Observer_gol()
    torcer_warg = Torcer.Observer_warg()
    await observar.assistir(torcer_penal)
    await observar.assistir(torcer_yellow)
    await observar.assistir(torcer_red)
    await observar.assistir(torcer_cantos)
    await observar.assistir(torcer_gol)
    await observar.assistir(torcer_warg)
    await observar.atualizacao("Canto", "42'", "EGR")
    await observar.atualizacao("Canto", "43'", "EGR")
    await observar.atualizacao("Fim do primeiro tempo", "999", "EGR")
    await observar.atualizacao("Canto", "46", "EGR")
    await observar.atualizacao("Canto", "47", "EGR")
    await observar.atualizacao("Canto", "48", "EGR")
    await observar.atualizacao("Gol", "48", "EGR")
    await observar.atualizacao("Gol", "48", "EGR")



if __name__ == '__main__':
    asyncio.run(main())