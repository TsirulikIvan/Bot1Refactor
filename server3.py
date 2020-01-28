import telebot
from telebot import types
from session2 import Session
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


@bot.message_handler(content_types=['text'])
def sessions_manager(message):
    if message.from_user.id in sessions.keys():
        sessions[message.from_user.id].handle(message)
    else:
        sessions.update([(message.from_user.id, Session())])


@bot.message_handler(commands=['help'])
def help_call(message):
    print(message.from_user.id)
    print(message.chat.id)
    bot.send_message(message.from_user.id, 'Для начала работы введите /start\n')


@bot.message_handler(commands=['start'])
def handler_of_other(message):
    bot.send_message(message.from_user.id, 'Для вызова подсказки введите /help')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    print(call.message)
    if call.data == 'accept':
        bot.send_message(call.message.chat.id, 'Отлично! Приступим к регистрации.\n Введите ваше имя')
        bot.register_next_step_handler(call.message, get_name)
    elif call.data == 'start_search':
        pass
    elif call.data == 'cancel_search':
        pass
    elif call.data == 'test1':
        pass
    elif call.data == 'test2':
        pass
    elif call.data == 'cancel_search':
        pass


@bot.message_handler(content_types=['text'])
def get_name(message):
    print('state 4')
    user_data = [message.from_user.id, message.text]
    bot.send_message(message.chat.id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    print('state 5')
    data.append(message.text)
    bot.send_message(message.chat.id, 'Введите название вашей компании:')
    bot.register_next_step_handler(message, get_company)


def get_company(message):
    print('state 6')
    append(message.text)
    bot.send_message(message.chat.id, 'Введите ваш телефон (в формате 8):')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    print('state 7')
    data.append(message.text)
    bot.send_message(message.chat.id, 'Регистрация завершена!')
    ctrl.add_record(tuple(data))


bot.polling()
