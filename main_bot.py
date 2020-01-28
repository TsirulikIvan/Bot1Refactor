import telebot
from telebot import types
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
data = {}


@bot.message_handler(commands=['start'])
def handler_of_other(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Принять соглашение', callback_data='accept')  # кнопка «Да»
    keyboard.add(key_yes)
    bot.send_message(message.from_user.id, 'Добро пожаловать!\n'
                                           'https://teletype.in/@sellwell/r1AkRWraH'
                     , reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def help_msg(message):
    bot.send_message(message.from_user.id, 'Команды:\n/start - начать работу с ботом\n/help - вывод справки')


def get_name(message):
    print('state 4')
    data[message.from_user.id].append(message.text)
    bot.send_message(message.from_user.id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    print('state 5')
    data[message.from_user.id].append(message.text)
    bot.send_message(message.from_user.id, 'Введите название вашей компании:')
    bot.register_next_step_handler(message, get_company)


def get_company(message):
    print('state 6')
    data[message.from_user.id].append(message.text)
    bot.send_message(message.from_user.id, 'Введите ваш телефон (в формате 8):')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    print('state 7')
    data[message.from_user.id].append(message.text)
    keyboard = types.InlineKeyboardMarkup()
    key = types.InlineKeyboardButton(text='Нет промокода', callback_data='no_code')
    keyboard.add(key)
    bot.send_message(message.from_user.id, 'Регистрация завершена!\n'
                                           'у вас есть код группы(промокод)\n'
                                           'который вам выдали в начале обучения?',
                     reply_markup=keyboard)

def get_code(message):

    data[message.from_user.id].append(message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'accept':
        bot.send_message(call.message.from_user.id, 'Отлично! Введите ваше имя:')
        data.update([(call.message.from_user.id, [call.message.from_user.id])])
        bot.register_next_step_handler(call.message, get_name)
    elif call.data == 'have_code':
        bot.send_message(call.message.from_user.id, 'Прекрасно! Введите его:')
        bot.register_next_step_handler(call.message, get_code)
    elif call.data == 'no_code':
        ctrl.add_record(tuple(data[call.message.from_user.id]))


bot.polling()