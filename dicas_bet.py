class Dicasbet:
    def __init__(self, horario, casa, fora, palpite, por_casa, por_empate, por_fora, primeiro_casa, primeiro_empate,
                 primeiro_fora, over1, over2, over3, am, an):
        self.horario = horario
        self.casa = casa
        self.fora = fora
        self.palpite = palpite
        self.por_casa = por_casa
        self.por_empate = por_empate
        self.por_fora = por_fora
        self.primeiro_casa = primeiro_casa
        self.primeiro_empate = primeiro_empate
        self.primeiro_fora = primeiro_fora
        self.over1 = over1
        self.over2 = over2
        self.over3 = over3
        self.am = am
        self.an = an

    def mostrar(self):
        texto = f'''<b>
🕐 {self.horario}
🔴 {self.casa}
⚫️ {self.fora}
✅ {self.palpite}
✅🔴 {self.por_casa} %
🔴 = ⚫️ {self.por_empate} %
✅⚫️ {self.por_fora} %
1ºT ✅🔴 {self.primeiro_casa} %
1ºT 🔴 = ⚫️ {self.primeiro_empate} %
1ºT ✅⚫️ {self.primeiro_fora} %
🔝🥅 1.5 = {self.over1} %
🔝🥅 2.5 = {self.over2} %
🔝🥅 3.5 = {self.over3} %
🔴⚫️🥅 {self.am} % 
🔴⚫️✖️🥅 {self.an} %
</b>
'''

        return texto
