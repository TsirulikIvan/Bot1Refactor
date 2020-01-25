import time
from session import Session
import telebot
from telebot import types
from db_controller import Controller
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv('API_TOKEN')
ctrl = Controller('base.db')
bot = telebot.TeleBot(API_TOKEN)


def clock(func):
    def clocked(*args, **kwargs):
        t0 = time.time()

        result = func(*args, **kwargs)  # вызов декорированной функции

        elapsed = time.time() - t0
        name = func.__name__
        arg_1st = []
        if args:
            arg_1st.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_1st.append(', '.join(pairs))
        arg_str = ', '.join(arg_1st)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked




@clock
def creating_sess(numbers):
    sessions = {}
    for i in range(numbers):
        sessions.update([(i, Session(i, ctrl, bot))])
    return sessions


print('15 = ', creating_sess(15))
print('30 = ', creating_sess(15))
print('60 = ', creating_sess(15))
