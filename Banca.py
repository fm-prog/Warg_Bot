ativo = False

class Gest_Banca:

    def __init__(self, saldo):
        self.saldo = saldo
        self.ganhos = []
        self.perdas = []

    async def get_saldo(self):
        return self.saldo

    async def get_ganhos(self):
        return self.ganhos

    async def get_perdas(self):
        return self.perdas

    async def set_saldo(self, valor):
        self.saldo = valor

    async def set_perdas(self, valor):
        self.perdas = valor

    async def set_ganhos(self, valor):
        self.ganhos = valor


Bnc = Gest_Banca(100)

