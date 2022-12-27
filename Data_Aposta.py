import pandas as pd
from pathlib import Path


class Inter_csv:

    @staticmethod
    async def write_csv(casa, fora, dados):
        times = [casa, fora]
        tempo = ""
        lista_dados = dados
        lista_dados = lista_dados.split("|")
        print(lista_dados)
        placar = [lista_dados[0], lista_dados[1]]

        tabela = pd.DataFrame(
            data=zip(times, placar),
            columns=["Times", "Placar:"]
        )

        for ind, item in enumerate(lista_dados):
            if ind == 2:
                tempo = lista_dados[2].replace(":", "+")
            elif ":" in item:
                tabela[lista_dados[ind]] = lista_dados[ind + 1], lista_dados[ind + 2]
                print(lista_dados[ind + 1])
                print(lista_dados[ind + 2])

        path = Path(f'Dados Apostador/{casa} x {fora} - {tempo}.csv')
        path.parent.mkdir(parents=True, exist_ok=True)
        tabela.to_csv(path)
