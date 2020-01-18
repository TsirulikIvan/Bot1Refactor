import telebot
from telebot import types
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def reg_func(msg):
    bot.send_message(msg.chat.id, 'Отлично! Приступим к регистрации. \nВведите ваше имя:')
    pass

@bot.message_handler(commands=['start'])
def auth_func(message):
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Принять соглашение', callback_data='accept');  # кнопка «Да»
    keyboard.add(key_yes);
    bot.send_message(message.chat.id, 'https://teletype.in/@sellwell/r1AkRWraH', reply_markup = keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    run = True
    while run:
        if call.data == "accept":
            run = False
            reg_func(call.message)

@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, 'Команды:\n/start - начать работу с ботом\n/help - вывод справки')




bot.polling()