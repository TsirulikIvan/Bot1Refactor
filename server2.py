import telebot
from session import Session
from db_controller import Controller
import os
from dotenv import load_dotenv
import time
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv('API_TOKEN')
ctrl = Controller('base.db')
bot = telebot.TeleBot(API_TOKEN)
sessions = {}
competitions = []


def search_func():
    print('search_func')
    for i in sessions:
        print(i)
        print(i.in_competition)
        if i.ready:
            competitions.append(i)


@bot.message_handler(commands=['help'])
def help(message):
    print(message.from_user.id)
    print(message.chat.id)
    bot.send_message(message.from_user.id, 'Для начала работы введите /start\n')


@bot.message_handler(commands=['start'])
def session_control_func(message):
    print('auth_func')
    if message.from_user.id in sessions.keys():
        print('in session')
        sessions[message.from_user.id].checked_reg_func(message)
        see_states()
    else:
        print('not in session')
        sessions.update([(message.from_user.id, Session(message, ctrl, bot))])
        see_states()


@bot.message_handler(content_types=['text'])
def handler(message):
    bot.send_message(message.from_user.id, 'Для вызова подсказки введите /help')


def see_states():
    print('states_func')
    for i in sessions.values():
        print('{0} : is ready to competition - {1}'.format(i, i.ready))



bot.polling()

