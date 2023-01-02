from traceback import format_tb

import pandas as pd
from pathlib import Path


class Inter_csv:

    @staticmethod
    async def rem_csv():
        p = Path('Dados Apostador')
        if p.exists():
            for child in p.iterdir():
                child.unlink()
            p.rmdir()
            return True
        else:
            return False

    @staticmethod
    async def write_csv(casa, fora, dados):
        lista_col = []
        lista_data = []
        lista_dados = dados
        lista_dados = lista_dados.split("|")
        print(dados)

        if Path(f'Dados Apostador/{casa} x {fora}.csv').exists():
            path = Path(f'Dados Apostador/{casa} x {fora}.csv')
            tabela = pd.read_csv(path, sep=",")
            print("O jogo está sendo monitorado, vou adicionar mais infos!")
            lista_col.append('Tempo')
            lista_data.append(lista_dados[2])
            lista_col.append(casa)
            lista_data.append(lista_dados[0])
            lista_col.append(fora)
            lista_data.append(lista_dados[1])

            for ind, item in enumerate(lista_dados):
                if ind == 2:
                    pass
                elif ":" in item:
                    lista_col.append(lista_dados[ind])
                    lista_data.append(lista_dados[ind + 1])

            df = pd.DataFrame([lista_data], columns=lista_col)

            path = Path(f'Dados Apostador/{casa} x {fora}.csv')

            if int(df.shape[1]) > int(tabela.shape[1]):
                print("Tabela de agora maior que a anterior!")
                tf = pd.DataFrame(tabela, columns=df.columns)
                tf = pd.concat([tf, df])
                tf = tf.fillna(0)
                tf.to_csv(path, index=False)
            else:
                print("Tabela menor ou igual!")
                tabela = pd.concat([tabela, df])
                tabela.to_csv(path, index=False)

        else:
            print("O jogo não está sendo monitorado, vou adicionar as infos!")
            tabela = pd.DataFrame(
                [
                    {'Tempo': lista_dados[2],
                     casa: lista_dados[0],
                     fora: lista_dados[1]
                     },
                ])

            for ind, item in enumerate(lista_dados):
                if ind == 2:
                    pass
                elif ":" in item:
                    tabela[lista_dados[ind]] = lista_dados[ind + 1]

            path = Path(f'Dados Apostador/{casa} x {fora}.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            tabela.to_csv(path, index=False)
