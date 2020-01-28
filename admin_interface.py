import telebot
import hashlib
from telebot import types
from db_controller import Controller
import os
from dotenv import load_dotenv
import time
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv('API_TOKEN2')
ctrl = Controller('base.db')
bot = telebot.TeleBot(API_TOKEN)
all_data = ctrl.query_adm_data('admins', ('name', 'surname', 'pass'))
users = {}
for i in all_data:
    print(i)
    tmp = list(i)[0:2]
    users.update([(i[2], tuple(tmp))])
print(users)


def auth(message):
    tmp = message.text
    print(bytes)
    password = hashlib.sha3_256().hexdigest()
    if password in users.keys():
        bot.send_message(message.from_user.id, 'Здравствуй, ' + ' '.join(users[password]))


@bot.message_handler(commands=['start'])
def first_state(message):
    bot.send_message(message.from_user.id, 'Приветствую!\n'
                                           ' Чтоб воспользоваться данным ботом введите пароль')
    bot.register_next_step_handler(message, auth)


bot.polling()
