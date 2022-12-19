from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
import asyncio
# list of storages, you can use any storage
from telebot.asyncio_storage import StateMemoryStorage
from telebot.async_telebot import types

# new feature for states.
from telebot.asyncio_handler_backends import State, StatesGroup

# default state storage is statememorystorage
bot = AsyncTeleBot('5638118272:AAH4v1fgYs9twpCjCmrMo08FMvT2KMolzWk', state_storage=StateMemoryStorage())
markup = types.ForceReply(selective=False)

# Just create different statesgroup
class MyStates(StatesGroup):
    name = State()  # statesgroup should contain states
    surname = State()
    age = State()


class Escolhas():
    texto_op1 = ""
    texto_op2 = ""
    funcao = None


# set_state -> sets a new state
# delete_state -> delets state if exists
# get_state -> returns state if exists


async def mostrar(op1, op2):
    return print(f"{op1} e {op2}")


@bot.message_handler(commands=['start'])
async def start_ex(message):
    """
    Start command. Here we are starting state
    """
    await bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    await bot.send_message(message.chat.id, 'Hi, write me a name', reply_markup=markup)

    Escolhas.funcao = mostrar


@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.name)
async def name_get(message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    await bot.send_message(message.chat.id, f'Now write me a surname')
    Escolhas.texto_op1 = 'Now write me a surname'
    await bot.set_state(message.from_user.id, MyStates.surname, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=MyStates.surname)
async def ask_age(message):
    """
    State 2. Will process when user's state is MyStates.surname.
    """
    await bot.send_message(message.chat.id, "What is your age?")
    Escolhas.texto_op2 = "What is your age?"
    await bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text


# result
@bot.message_handler(state=MyStates.age, is_digit=True)
async def ready_for_answer(message):
    """
    State 3. Will process when user's state is MyStates.age.
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        await bot.send_message(message.chat.id,
                               "Ready, take a look:\n<b>Name: {name}\nSurname: {surname}\nAge: {age}</b>".format(
                                   name=data['name'], surname=data['surname'], age=message.text), parse_mode="html")
    await bot.delete_state(message.from_user.id, message.chat.id)
    await Escolhas.funcao(Escolhas.texto_op1, Escolhas.texto_op2)


# incorrect number
@bot.message_handler(state=MyStates.age, is_digit=False)
async def age_incorrect(message):
    """
    Will process for wrong input when state is MyState.age
    """
    await bot.send_message(message.chat.id,
                           'Looks like you are submitting a string in the field age. Please enter a number')


# register filters

bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(asyncio_filters.IsDigitFilter())

asyncio.run(bot.polling())
