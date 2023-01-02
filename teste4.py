import asyncio
import random
from traceback import format_tb

import pandas as pd
from pathlib import Path

from playwright.async_api import async_playwright


async def main():
    casa = "Lecce"
    fora = "NK Varazdin"
    times = [casa, fora]
    tempo = ""
    lista_dados = ['1', '0', '20:14', 'Cartões Amarelos US Lecce:', '1', 'Cartões Amarelos NK Varazdin:', '0',
                   'Cartões Vermelhos US Lecce:', '1', 'Cartões Vermelhos NK Varazdin:', '1', 'Escanteios US Lecce:',
                   '0', 'Escanteios NK Varazdin:', '1', 'Posse de bola US Lecce:', '54', 'Posse de bola NK Varazdin:',
                   '45', 'Fatos do jogo']
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

        df = pd.DataFrame([lista_data], columns=lista_col)
        print(tabela)
        print(df)
        tabela = tabela.append(df)
        path = Path(f'Dados Apostador/{casa} x {fora}.csv')
        path.parent.mkdir(parents=True, exist_ok=True)
        tabela.to_csv(path, index=False)


if __name__ == '__main__':
    asyncio.run(main())
