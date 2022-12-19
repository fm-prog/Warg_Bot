from traceback import format_tb

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot('Warg')


async def treinar_bot(msg_user, reply):
    conversa = []
    trainer = ListTrainer(chatbot)
    conversa.append(msg_user)
    conversa.append(reply)
    try:
        trainer.train(conversa)
        return "<b>✅ Sucesso! Estou aprendendo contigo!</b>"
    except Exception as error:
        print(f"Deu merda, aqui o que foi: {error.__class__}")
        print(error)
        print(format_tb(error.__traceback__))
        return "<b>❌ Foi mal, deu algum erro!</b>"


async def intergrade(mensagem):
    try:
        return chatbot.get_response(mensagem)
    except Exception as error:
        print(f"Deu merda, aqui o que foi: {error.__class__}")
        print(error)
        print(format_tb(error.__traceback__))
        return "❌ Foi mal, deu algum erro!"



