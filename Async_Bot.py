import datetime
import logging
import asyncio
import aioschedule
from telebot.async_telebot import AsyncTeleBot
from telebot.async_telebot import types
import Apostador
import Banca
import Motor_DicasBet
from Motor_live import MotorLive
import Warg
import Func_Lib as Lib
import Proto_IA as IA
import telebot.util
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot import asyncio_filters

logging.basicConfig(level=logging.DEBUG, filename="Bot.log", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger('TeleBot')
logger.setLevel(logging.DEBUG)

token = '5638118272:AAH4v1fgYs9twpCjCmrMo08FMvT2KMolzWk'
bot = AsyncTeleBot(token)
markup = types.ForceReply(selective=False)

sch_atualizacao = aioschedule.Scheduler()
sch_monitoramento = aioschedule.Scheduler()
sch_agendar = aioschedule.Scheduler()
sch_programar = aioschedule.Scheduler()
sch_supervisor = aioschedule.Scheduler()
sch_apostador = aioschedule.Scheduler()


class MyStates(StatesGroup):
    program_op1 = State()
    program_op2 = State()
    treinar_op1 = State()
    treinar_op2 = State()


@bot.message_handler(commands=['ajuda'])
async def responder(mensagem):
    """
    Função que mostra pro usuário os comandos disponíveis!
    """
    texto = f'''
⚠️ Comandos

🫡 /live - Lista de jogos ao vivo! 
🫡 /dicas_bet - Dicas de apostas para hoje do site DicasBet!
🫡 /leve - Ativa ou desativa o modo de economia de memória!
🫡 /agendar_off - Desativa todos os lembretes de jogos ao vivo!
🫡 /alive - Verifica se o Bot está Online!
🫡 /monitorados - Mostra quais jogos estão!
🫡 /treinar - Comando para treinar o Bot com perguntas e respostas!
🫡 /programar - Programa a busca de um determinado jogo em uma determinada hora!
🫡 /cancelar - Cancela a digitação de qualquer opção de um comando!
🫡 /programar_off - Desmarca todas as programações feitas!
🫡 /banca - Ativa ou desativa a função Gestão de Banca!
🫡 /get_saldo - Mostra ao usuário o saldo da banca!
🫡 /apostador - Ativa a função Apostador!
🫡 /drop (número) - Função que dropa um observador!
✅Exemplo: /drop 1
🫡 /agendar (minutos) - Função que agenda atualizações de jogos online a cada período determinado!
✅Exemplo: /agendar 60
🫡 /torcer (nome) - Função para monitorar um determinado jogo de um determinado time!
✅Exemplo: /torcer Bahia
🫡 /set_saldo (valor) - Função para definir o saldo da Banca!
✅Exemplo: /set_saldo 100
'''
    if len(str(texto)) > 4096:
        for x in range(0, len(str(texto)), 4096):
            await bot.send_message(mensagem.chat.id, f"<b>{texto[x:x + 4096]}</b>", parse_mode="HTML")
    else:
        await bot.reply_to(mensagem, f"<b>{texto}</b>", parse_mode="HTML")


@bot.message_handler(commands=['drop'])
async def responder(mensagem):
    """
    Função que dropa um observador!
    """
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    arg = telebot.util.extract_arguments(mensagem.text)
    if await Lib.is_drop(arg):
        match arg:
            case "1":
                if Warg.monitorados[0] != "Stand By":
                    Warg.monitorados[0] = "Close"
                    await bot.reply_to(mensagem, "<b>✅ Flw, o Observador 1 está se despedindo da galera!</b>",
                                       parse_mode="HTML")
                else:
                    await bot.reply_to(mensagem, "<b>⛔️ Este observador está desocupado!</b>", parse_mode="HTML")
            case "2":
                if Warg.monitorados[1] != "Stand By":
                    Warg.monitorados[1] = "Close"
                    await bot.reply_to(mensagem, "<b>✅ Flw, o Observador 2 está se despedindo da galera!</b>",
                                       parse_mode="HTML")
                else:
                    await bot.reply_to(mensagem, "<b>⛔️ Este observador está desocupado!</b>", parse_mode="HTML")
            case "3":
                if Warg.monitorados[2] != "Stand By":
                    Warg.monitorados[2] = "Close"
                    await bot.reply_to(mensagem, "<b>✅ Flw, o Observador 3 está se despedindo da galera!</b>",
                                       parse_mode="HTML")
                else:
                    await bot.reply_to(mensagem, "<b>⛔️ Este observador está desocupado!</b>", parse_mode="HTML")
            case "4":
                if Warg.monitorados[3] != "Stand By":
                    Warg.monitorados[3] = "Close"
                    await bot.reply_to(mensagem, "<b>✅ Flw, o Observador 4 está se despedindo da galera!</b>",
                                       parse_mode="HTML")
                else:
                    await bot.reply_to(mensagem, "<b>⛔️ Este observador está desocupado!</b>", parse_mode="HTML")
            case "5":
                if Warg.monitorados[4] != "Stand By":
                    Warg.monitorados[4] = "Close"
                    await bot.reply_to(mensagem, "<b>✅ Flw, o Observador 5 está se despedindo da galera!</b>",
                                       parse_mode="HTML")
                else:
                    await bot.reply_to(mensagem, "<b>⛔️ Este observador está desocupado!</b>", parse_mode="HTML")
    else:
        await bot.reply_to(mensagem, "<b>⚠️ Por favor colocar o comando drop, seguido de um número de 1 a "
                                     "5!\n✅ Exemplo: /drop 1</b>", parse_mode="HTML")


@bot.message_handler(commands=['alive'])
async def responder(mensagem):
    """
    Função que retorna status do bot!
    """
    await bot.send_sticker(mensagem.chat.id, "CAACAgIAAxkBAAEGMYhjV9XtE9nMmjHHixuu8GamIPOgbwACVAADQbVWDGq3-McIjQH6KgQ")
    await bot.reply_to(mensagem,
                       "<b>⚠️ Opa, to on!\nQualquer coisa me chama!\nSe quiser que eu observe algum jogo, só me manda: "
                       "torcer "
                       "Nome do Time</b>",
                       parse_mode="HTML")


@bot.message_handler(commands=['dicasbet'])
async def responder(mensagem):
    """
    Função que retorna as dicas do Dicas Bet
    """
    await bot.reply_to(mensagem, "Pera que vou ver no Dicas Bet pra ti!")
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    dicas = Motor_DicasBet.dicas_dicasbet()
    dica = ""
    print(len(dicas))
    for i in range(len(dicas)):
        if i == 19 or i == 39 or i == 59 or i == 79 or i == 99 or i == 119 or i == 139 or i == 159 or i == 179 or i == 199:
            dica = dica + dicas[i]
            print(dica)
            await bot.reply_to(mensagem, dica, parse_mode="HTML")
            dica = ""
        dica = dica + dicas[i]
    await bot.send_message(mensagem.chat.id,
                           "<b>\n⚠️ Peguei la no Dicas Bet:\n\nhttps://dicasbet.com.br/palpites-de-futebol/\n\nSite que tem "
                           "ótimas dicas de apostas!</b>",
                           parse_mode="HTML")


@bot.message_handler(commands=['leve'])
async def responder(mensagem):
    """
    Ativar ou desativa o modo de economia de memória!
    """
    if Warg.low_mem:
        Warg.low_mem = False
        await bot.reply_to(mensagem, "<b>❌ Modo de economia de memória desativado!</b>", parse_mode="HTML")
    else:
        Warg.low_mem = True
        await bot.reply_to(mensagem, "<b>✅ Modo de economia de memória ativado!</b>", parse_mode="HTML")


@bot.message_handler(commands=['live'])
async def responder(mensagem):
    """
    Retorna os jogos ao vivo!
    """
    await bot.reply_to(mensagem, "<b>Pera que vou ver na Betano pra ti!</b>", parse_mode="HTML")
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    jogos = await MotorLive.mostrar_jogos_live()
    for i in jogos:
        await bot.send_message(mensagem.chat.id, i, parse_mode="HTML")
    await bot.send_message(mensagem.chat.id,
                           f"\n<b>⚠️ Peguei la na Betano:\n\nhttps://br.betano.com/live/\n \nSe liga lá, a casa de "
                           f"apostas mais recomendada!</b>\n",
                           parse_mode="HTML")


async def atualizacao_live(message):
    """
    Função que atualiza os jogos ao vivo, chamada pela função agendadora!
    """
    await bot.send_chat_action(message.chat.id, 'typing')
    await bot.reply_to(message, "<b>⚠️ Como agendado, vou listar os jogos online!</b>",
                       parse_mode="HTML")
    jogos = await MotorLive.mostrar_jogos_live()
    for i in jogos:
        await bot.send_message(message.chat.id, i, parse_mode="HTML")
    await bot.send_message(message.chat.id,
                           f"\n<b>⚠️ Peguei la na Betano:\n\nhttps://br.betano.com/live/\n \nSe liga lá, a casa de "
                           f"apostas mais recomendada!</b>\n",
                           parse_mode="HTML")


async def atualizacao_apostador(msg):
    """
    Função que verifica se há atualizações no Apostador, caso hajam, as informam para o usuário!
    """
    if Apostador.infos:
        for i in Apostador.infos:
            print(f"Fila de Atualização: {Apostador.infos}")
            print(f"Vai atualizar: {i}")
            await bot.send_chat_action(msg.chat.id, 'typing')
            await bot.send_message(msg.chat.id, i, parse_mode="HTML")
            index = Apostador.infos.index(i)
            del (Apostador.infos[index])
            print(f"Ainda na fila: {Apostador.infos}")


async def atualizacao_lance(msg):
    """
    Função que verifica se há atualizações, caso hajam as informam para o usuário!
    """
    if Warg.infos:
        for i in Warg.infos:
            print(f"Fila de Atualização: {Warg.infos}")
            print(f"Vai atualizar: {i}")
            await bot.send_chat_action(msg.chat.id, 'typing')

            if "Escanteio!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMldjV_HVgjjxmO2nC0ZAmeMpxaUurAACngEAAiUDUg9fX4PZyRKR1ioE")

            if "O jogo deve ter acabado!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMkVjV-zoHom9oKHc5tYqMe8-4uMTdQACtAEAAiUDUg9XeXrk5OGqGCoE")

            if "Acabou!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMkdjV-14-JdMoWVTlYWR3NxzjUhFHQACoQEAAiUDUg_jjpHkoQdmtioE")

            if "voltarão quando o intervalo acabar!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMjVjV-xuv736wtChYKSm87a_ltvXtQACugEAAiUDUg8cu4dj66hOTSoE")

            if "Perdeu!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGU1xjZuNq7ZMnY0W7DlP-o4qZ-2qcBgACnwEAAiUDUg_p3654CM787isE")
            elif "Penal!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMiJjV-t9AVhG-pspJFGXVKc7eeZI1gACqwEAAiUDUg-NSub-63qRDyoE")

            if "Anulou!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGU0ljZtR6Rn3ppCLzlThlif7CXovRQQACuAEAAiUDUg_Ww2TtNwoBzisE")
            elif "Gol!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMiRjV-uR1Nj-p2JS3_iQz5zV8ydHsAACsQEAAiUDUg8yym_aWi0vkioE")

            if "Cartão Amarelo!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMiZjV-upv_a4DezXMsKPIn2I3EbNMgACqQEAAiUDUg9ScUw7XLSgcioE")

            if "Cartão Vermelho!" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMihjV-u6ebtWnDOnNjeJkCzPlvhoEwACsAEAAiUDUg_Z653V0NNSpSoE")

            if "deixou de acompanhar o jogo" in i:
                await bot.send_sticker(msg.chat.id,
                                       "CAACAgIAAxkBAAEGMY5jV9cNETQZZSeg1XHnJfULac87JwACUgADQbVWDAIQ4mRpfw9yKgQ")

            await bot.send_message(msg.chat.id, i, parse_mode="HTML")
            index = Warg.infos.index(i)
            del (Warg.infos[index])
            print(f"Ainda na fila: {Warg.infos}")


async def monitoramento(msg):
    """
    Função que retorna os jogos monitorados!
    """
    desocup = ""
    await bot.send_message(msg.chat.id, "<b>👁‍🗨 Monitoramento...</b>", parse_mode="HTML")
    for t, i in enumerate(Warg.monitorados):
        await bot.send_chat_action(msg.chat.id, 'typing')
        if i == "Close":
            await bot.send_message(msg.chat.id, f"<b>👁‍🗨 O Observador {t + 1} está se despedindo da galera!\n</b>",
                                   parse_mode="HTML")
        elif i != "Stand By":
            await bot.send_message(msg.chat.id, i, parse_mode="HTML")
        else:
            desocup += f"<b>👁‍🗨 O Observador {t + 1} está desocupado!\n</b>"

    if desocup != "":
        await bot.send_chat_action(msg.chat.id, 'typing')
        await bot.send_sticker(msg.chat.id, "CAACAgIAAxkBAAEGMaRjV9hH3th0IoUpQDFyvkkMsQ61KwACUAADQbVWDEsUyxvLOcdYKgQ")
        await bot.send_message(msg.chat.id, desocup, parse_mode="HTML")


@bot.message_handler(commands=['monitorados'])
async def responder(mensagem):
    """
    Função que chama a função monitoramento!
    """
    await monitoramento(mensagem)


@bot.message_handler(commands=['agendar_off'])
async def responder(mensagem):
    """
    Função que cancela todos os agendamentos!
    """
    sch_agendar.clear()
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.reply_to(mensagem, "<b>⚠️ Todo(s) o(s) agendamento(s) for(am) desmarcado(s)!</b>", parse_mode="HTML")


@bot.message_handler(commands=['agendar'])
async def responder(mensagem):
    """
    Função que agenda atualizacoes!
    """
    tempo = mensagem.text
    tempo = telebot.util.extract_arguments(tempo)
    if await Lib.is_agendar(tempo):
        await bot.reply_to(mensagem, "<b>⚠️ Pera que vou agendar pra ti!</b>", parse_mode="HTML")
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        sch_agendar.every(int(tempo)).minutes.do(atualizacao_live, message=mensagem)
        await bot.reply_to(mensagem, f"<b>⚠️ Agendadas atualizações de jogos ao vivo a cada: {tempo} minuto(s)!</b>",
                           parse_mode="HTML")
    else:
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>⚠️ Por favor colocar o comando /agendar, seguido de um número de 1 a "
                                     "999!\n✅ Exemplo: /agendar 60</b>", parse_mode="HTML")


@bot.message_handler(commands=['programar'])
async def responder(mensagem):
    """
    Função para programar jogos!
    """
    await bot.set_state(mensagem.from_user.id, MyStates.program_op1, mensagem.chat.id)
    await bot.send_message(mensagem.chat.id, "<b>⚠️ Certo, me diz qual é o nome de um dos times que vão jogar!</b>",
                           parse_mode="HTML", reply_markup=markup)


@bot.message_handler(state="*", commands=['cancelar'])
async def any_state(mensagem):
    """
    Cancelar qualquer opção
    """
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.send_message(mensagem.chat.id, "<b>⚠️ Blz, cancelei a digitação da opção!</b>", parse_mode="HTML")
    await bot.delete_state(mensagem.from_user.id, mensagem.chat.id)


@bot.message_handler(state=MyStates.program_op1)
async def programar_op1(mensagem):
    """
        Opção 1 para o programar (time)
    """
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.send_message(mensagem.chat.id, "<b>⚠️ Agora me diz o horário que tu quer que eu procure esse jogo!</b>",
                           parse_mode="HTML", reply_markup=markup)
    await bot.set_state(mensagem.from_user.id, MyStates.program_op2, mensagem.chat.id)
    async with bot.retrieve_data(mensagem.from_user.id, mensagem.chat.id) as data:
        data['program_op1'] = mensagem.text


@bot.message_handler(state=MyStates.program_op2)
async def programar_op2(mensagem):
    """
        Opção 2 para o programar (Hora)
    """
    if await Lib.is_programar(mensagem.text):
        async with bot.retrieve_data(mensagem.from_user.id, mensagem.chat.id) as data:
            sch_programar.every(1).second.do(programar_sch, mensagem=mensagem, time=data['program_op1'],
                                             hora=mensagem.text)
            await bot.send_chat_action(mensagem.chat.id, 'typing')
            await bot.reply_to(mensagem,
                               f"<b>⚠️ Pronto! Às {mensagem.text} vou procurar o jogo do(e)(a) {data['program_op1']} pra ti!</b>",
                               parse_mode="HTML")
            print(sch_programar.jobs)
        await bot.delete_state(mensagem.from_user.id, mensagem.chat.id)
    else:
        await bot.reply_to(mensagem,
                           "<b>⚠️ Por favor, informe corretamente o horário que deseja monitorar!\n\n✅ Exemplo: 21:00:00</b>",
                           parse_mode="HTML", reply_markup=markup)
        await bot.reply_to(mensagem,
                           "<b>⚠️ Observe algumas regras:\n\n✅ Agendamentos podem ser feitos no mínimo para o próximo minuto!\n\n✅ Preste atenção à limitação do formato: 23:59:59\n\n✅ Agendamentos podem ser feitos somente para o dia atual!</b>",
                           parse_mode="HTML")


@bot.message_handler(commands=['programar_off'])
async def responder(mensagem):
    """
    Função que cancela todas as programações!
    """
    sch_programar.clear()
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.reply_to(mensagem, "<b>⚠️ As programações foram desmarcadas!</b>", parse_mode="HTML")


@bot.message_handler(commands=['torcer'])
async def responder(mensagem):
    """
    Função para monitorar jogos!
    """
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.reply_to(mensagem, "<b>⚠️ Vou ver se o jogo já começou na Betano!</b>", parse_mode="HTML")
    pesquisa = mensagem.text
    pesquisa = telebot.util.extract_arguments(pesquisa)
    if await Lib.is_time(pesquisa):

        resposta = await Warg.torcer(pesquisa)

        if "Foi mal" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "não começou!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "já está sendo monitorado!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "estão ocupados!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        else:
            resposta = resposta + "\n<b>🏟 Tô de olho nesse jogo, qualquer lance importante te falo!</b>"
            await bot.send_chat_action(mensagem.chat.id, 'typing')
            await bot.reply_to(mensagem, resposta, parse_mode="HTML")
            await supervisionar(mensagem)
    else:
        await bot.reply_to(mensagem,
                           "<b>⚠️ Por favor, informe corretamente o nome de um time!\n\n✅ Exemplo: /torcer Bahia</b>",
                           parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=['banca'])
async def responder(mensagem):
    """
    Ativar ou desativa a função de gestão de banca!
    """
    if Banca.ativo:
        Banca.ativo = False
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>❌ Gestão de Banca desativada!</b>", parse_mode="HTML")
    else:
        Banca.ativo = True
        Banca.Bnc = Banca.Gest_Banca(100.00)
        print(await Banca.Bnc.get_saldo())
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>✅ Gestão de Banca ativada!</b>", parse_mode="HTML")
        await bot.reply_to(mensagem, "<b>✅ Banca criada com valor standard de 100 reais!</b>", parse_mode="HTML")


@bot.message_handler(commands=['set_saldo'])
async def responder(mensagem):
    """
    Setar saldo da banca!
    """
    if Banca.ativo:
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>⚠️ Pera que vou adicionar pra ti!</b>", parse_mode="HTML")
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        valor = mensagem.text
        valor = telebot.util.extract_arguments(valor)
        if await Lib.is_valor(valor):
            await Banca.Bnc.set_saldo(float(valor))
            print(await Banca.Bnc.get_saldo())
            await bot.reply_to(mensagem, f"<b>⚠️ O saldo da banca foi alterado para {valor} reais!</b>",
                               parse_mode="HTML")
        else:
            await bot.reply_to(mensagem,
                               f"<b>⚠️ Por favor, informe o comando de forma correta, exemplo: /set_saldo 300</b>",
                               parse_mode="HTML")
    else:
        await bot.reply_to(mensagem, "<b>⚠️ Ative primeiro a Gestão de Banca através do comando /banca!</b>",
                           parse_mode="HTML")


@bot.message_handler(commands=['get_saldo'])
async def responder(mensagem):
    """
    Mostra ao usuário o saldo da banca!
    """
    if Banca.ativo:
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>⚠️ Pera que vou ver o saldo pra ti!</b>", parse_mode="HTML")
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, f"<b>⚠️ O saldo da banca é de {await Banca.Bnc.get_saldo()} reais!</b>",
                           parse_mode="HTML")
        print(await Banca.Bnc.get_saldo())
    else:
        await bot.reply_to(mensagem, "<b>⚠️ Ative primeiro a Gestão de Banca através do comando /banca!</b>",
                           parse_mode="HTML")


@bot.message_handler(commands=['apostador'])
async def responder(mensagem):
    """
    Ativar a função apostador!
    """
    if Banca.ativo:
        apost = sch_apostador.jobs
        if apost:
            await bot.send_chat_action(mensagem.chat.id, 'typing')
            await bot.send_sticker(mensagem.chat.id,
                                   "CAACAgIAAxkBAAEG20ZjnN-hbxtmo2bLnqSAEbYTvC0UNwACngIAAzigCnbbnChT4sv5LAQ")
            await bot.reply_to(mensagem, "<b>❌ Função Apostador desativada!</b>", parse_mode="HTML")
            sch_apostador.clear()
            Apostador.ativo = False
            Apostador.infos = []
        else:
            await bot.send_chat_action(mensagem.chat.id, 'typing')
            await bot.send_sticker(mensagem.chat.id,
                                   "CAACAgIAAxkBAAEG20RjnN6d6qGFm7aIG2bDAoToOirNMwACmwIAAzigCnIiKYAfnhYoLAQ")
            await bot.reply_to(mensagem,
                               "<b>⚠️ Sucesso, vou gestionar a banca e mandar dicas de apostas pra tú, segue as calls, (ou não) 😂😂😂!</b>",
                               parse_mode="HTML")
            Apostador.ativo = True
            sch_apostador.every(2).seconds.do(atualizacao_apostador, msg=mensagem)
            await Apostador.monitorar()
    else:
        await bot.reply_to(mensagem, "<b>⚠️ Ative primeiro a Gestão de Banca através do comando /banca!</b>",
                           parse_mode="HTML")


@bot.message_handler(commands=['treinar'])
async def responder(mensagem):
    """
    Função para treinar o Bot!
    """
    await bot.set_state(mensagem.from_user.id, MyStates.treinar_op1, mensagem.chat.id)
    await bot.send_message(mensagem.chat.id, "<b>⚠️ Certo, me diz o modelo de pergunta do usuário para o bot!</b>",
                           parse_mode="HTML", reply_markup=markup)


@bot.message_handler(state=MyStates.treinar_op1)
async def responder(mensagem):
    """
    Opção 1 para o treinamento (Pergunta do usuário)
    """
    await bot.send_chat_action(mensagem.chat.id, 'typing')
    await bot.send_message(mensagem.chat.id, "<b>⚠️ Blz, me diz agora o modelo de resposta do bot para o usuário!</b>",
                           parse_mode="HTML", reply_markup=markup)
    await bot.set_state(mensagem.from_user.id, MyStates.treinar_op2, mensagem.chat.id)
    async with bot.retrieve_data(mensagem.from_user.id, mensagem.chat.id) as data:
        data['treinar_op1'] = mensagem.text


@bot.message_handler(state=MyStates.treinar_op2)
async def programar_op2(mensagem):
    """
        Opção 2 para o treinamento (Resposta do bot)
    """
    async with bot.retrieve_data(mensagem.from_user.id, mensagem.chat.id) as data:
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        response = await IA.treinar_bot(data['treinar_op1'], mensagem.text)

        if "Sucesso!" in str(response):
            await bot.send_sticker(mensagem.chat.id,
                                   "CAACAgIAAxkBAAEG35ljntu4N86ipjqCHNj4JRf-HEpG6AACmAIAAzigChdZHAHjHrETLAQ")
        else:
            await bot.send_sticker(mensagem.chat.id,
                                   "CAACAgIAAxkBAAEG35tjntxF_qdul6Rp1UcLsYTqWhdwewACmQIAAzigCs3VGh78Q5RNLAQ")

        await bot.reply_to(mensagem, response,
                           parse_mode="HTML")
    await bot.delete_state(mensagem.from_user.id, mensagem.chat.id)


async def programar_sch(mensagem, time, hora):
    """
    Função que checa e efetiva a programação!
    """

    time_now = datetime.datetime.now()
    time_now = time_now.strftime("%X")

    if hora == time_now:

        print("Farei a programacão!")
        await bot.send_chat_action(mensagem.chat.id, 'typing')
        await bot.reply_to(mensagem, "<b>⚠️ Como programado, vou ver se o jogo já começou na Betano!</b>",
                           parse_mode="HTML")

        resposta = await Warg.torcer(time)

        await bot.send_chat_action(mensagem.chat.id, 'typing')

        if "Foi mal" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "não começou!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "já está sendo monitorado!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        elif "estão ocupados!" in resposta:
            await bot.reply_to(mensagem, f"⚠️ <b>{resposta}</b>", parse_mode="HTML")

        else:
            resposta = resposta + "\n<b>🏟 Tô de olho nesse jogo, qualquer lance importante te falo!</b>"
            await bot.reply_to(mensagem, resposta, parse_mode="HTML")
            await supervisionar(mensagem)

        print(sch_programar.jobs)

        return aioschedule.CancelJob


@bot.message_handler(func=lambda message: True)
async def all_pms(message):
    """
    Função que recebe todas as mensagens e chama outra no prototipo da IA!
    """
    if await Lib.is_comand(message.text):
        msg = message.text
        msg = msg.replace("/", "")
    else:
        msg = message.text

    response = await IA.intergrade(msg)

    await bot.send_chat_action(message.chat.id, 'typing')

    if len(str(response)) > 4096:
        for x in range(0, len(str(response)), 4096):
            await bot.send_message(message.chat.id, f"<b>{response[x:x + 4096]}</b>", parse_mode="HTML")
    else:
        await bot.reply_to(message, f"<b>{response}</b>", parse_mode="HTML")


async def check_sch(msg):
    """
    Função que checa alguns parâmetros dos schedules!
    """

    atu = sch_atualizacao.jobs
    monit = sch_monitoramento.jobs
    if not Warg.paginas and not Warg.infos:
        if atu and monit:
            await bot.send_message(msg.chat.id, "<b>👁‍🗨 Não há observadores ocupados por enquanto!</b>",
                                   parse_mode="HTML")
            print(f"Dei Clear nos jobs!")
            sch_atualizacao.clear()
            sch_monitoramento.clear()

    if Warg.paginas:
        if not atu and not monit:
            sch_atualizacao.every(2).seconds.do(atualizacao_lance, msg=msg)
            sch_monitoramento.every(15).minutes.do(monitoramento, msg=msg)


async def supervisionar(mensagem):
    """
    Função que ativa schedules mestres!
    """

    supervisor = sch_supervisor.jobs
    print(f"Jobs do supervisor: {supervisor}")
    if not supervisor:
        print(f"Agendei Atualização, Monitoramento e supervisor!")
        sch_atualizacao.every(2).seconds.do(atualizacao_lance, msg=mensagem)
        sch_monitoramento.every(15).minutes.do(monitoramento, msg=mensagem)
        sch_supervisor.every(1).second.do(check_sch, msg=mensagem)


async def scheduler():
    """
    Função que da start nos schedules!
    """
    while True:
        await sch_agendar.run_pending()
        await sch_supervisor.run_pending()
        await sch_atualizacao.run_pending()
        await sch_monitoramento.run_pending()
        await sch_programar.run_pending()
        await sch_apostador.run_pending()
        await asyncio.sleep(1)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))


async def main():
    await asyncio.gather(bot.polling(non_stop=True), scheduler())


if __name__ == '__main__':
    asyncio.run(main())
