import telebot
import hashlib
from user import User
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


def create_admins_data_dict(data=('chat_id', 'pass')):
    res = {}
    tmp = ctrl.query_adm_data('admins', ','.join(data))
    for i in tmp:
        res.update([(i[0], i[1])])
    return res


admins = create_admins_data_dict()
print(admins)


def create_inline_markup(titles=('Общая статистика', 'Статистика по группам', 'Личный кабинет'),
                         callbacks=('full_stat', 'group_stat', 'profile')):
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=title, callback_data=callback_data)
               for title, callback_data in zip(titles, callbacks)]
    markup.add(*buttons)
    return markup


def auth(message):
    tmp = message.from_user.id
    if tmp in admins.keys() and hashlib.sha3_256(message.text.encode()).hexdigest() == admins[tmp]:
        bot.send_message(tmp, 'Добро пожаловать! 😊', reply_markup=create_inline_markup())
    else:
        bot.send_message(tmp,'Вы не входите в число администраторов\nили неправильно ввели пароль!🤔\n'
                         'Попробуйте еще раз.')
        bot.register_next_step_handler(message, auth)


@bot.message_handler(commands=['start'])
def first_state(message):
    bot.send_message(message.from_user.id, 'Приветствую!\n'
                                           'Чтоб воспользоваться данным ботом введите пароль')
    bot.register_next_step_handler(message, auth)


@bot.message_handler(commands=['/adding_new_admin'])
def add_admin(message):
    bot.send_message(message.from_user.id, 'Приветствую!\n')


@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    if call.data == 'full_stat':
        users_data = ctrl.query_all('users')


bot.polling()

