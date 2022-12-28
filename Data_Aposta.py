from traceback import format_tb

import pandas as pd
from pathlib import Path


class Inter_csv:

    @staticmethod
    async def write_csv(casa, fora, dados):
        times = [casa, fora]
        lista_dados = dados
        lista_dados = lista_dados.split("|")
        print(lista_dados)

        try:
            path = Path(f'Dados Apostador/{casa} x {fora}.csv')
            tabela = pd.read_csv(path, sep=",")
        except Exception as error:
            print(f"Deu merda, aqui o que foi: {error.__class__}")
            print(error)
            print(format_tb(error.__traceback__))

            tabela = pd.DataFrame(
                [
                    {'Tempo': lista_dados[2],
                     casa: lista_dados[0],
                     fora: lista_dados[1]
                     },
                ]
            )

            for ind, item in enumerate(lista_dados):
                if ind == 2:
                    pass
                elif ":" in item:
                    tabela[lista_dados[ind]] = lista_dados[ind + 1]

            path = Path(f'Dados Apostador/{casa} x {fora}.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            tabela.to_csv(path, index=False)
        else:
            lista_col = []
            lista_data = []
            lista_col.append(casa)
            lista_data.append(lista_dados[0])
            lista_col.append(fora)
            lista_data.append(lista_dados[1])
            lista_col.append('Tempo')
            lista_data.append(lista_dados[2])

            for ind, item in enumerate(lista_dados):
                if ind == 2:
                    pass
                elif ":" in item:
                    lista_col.append(lista_dados[ind])
                    lista_data.append(lista_dados[ind + 1])
                    # coluna = str(lista_dados[ind])
                    # tabela = tabela.append([{coluna: lista_dados[ind + 1]}])

            print(lista_col, lista_data)
            df = pd.DataFrame([lista_data], columns=lista_col)
            tabela = tabela.append(df)
            path = Path(f'Dados Apostador/{casa} x {fora}.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            tabela.to_csv(path, index=False)
