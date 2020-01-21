import telebot
from session import Session
from db_controller import Controller
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv('API_TOKEN')
ctrl = Controller('base.db')
bot = telebot.TeleBot(API_TOKEN)
sessions = {}


@bot.message_handler(commands=['start'])
def session_control_func(message):
    print('auth_func')
    if message.from_user.id in sessions.keys():
        print('in session')
        sessions[message.from_user.id].checked_reg_func(message)
    else:
        print('not in session')
        sessions.update([(message.from_user.id, Session(message, ctrl, bot))])



bot.polling()
