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


def reg_func(msg):
    print('I`m here')
    data = [msg.from_user.id]
    bot.send_message(msg.chat.id, 'Отлично! Приступим к регистрации. \nВведите ваше имя:')

    @bot.message_handler(content_types=['text'])
    def get_name(message):
        print('state 4')
        data.append(message.text)
        bot.send_message(message.chat.id, 'Введите вашу фамилию:')
        bot.register_next_step_handler(message, get_surname)

    def get_surname(message):
        print('state 5')
        data.append(message.text)
        bot.send_message(msg.chat.id, 'Введите название вашей компании:')
        bot.register_next_step_handler(message, get_company)

    def get_company(message):
        print('state 6')
        data.append(message.text)
        bot.send_message(msg.chat.id, 'Введите ваш телефон (в формате 8):')
        bot.register_next_step_handler(message, get_phone)

    def get_phone(message):
        print('state 7')
        data.append(message.text)
        bot.send_message(msg.chat.id, 'Регистрация завершена!')
        ctrl.add_record(tuple(data))
        bot.register_next_step_handler(message, auth_func)


def auth_func(message):
    print('state 1')
    key = ctrl.query_any_rows('chat_id', message.from_user.id)
    if key is None:
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура ge
        key_yes = types.InlineKeyboardButton(text='Принять соглашение', callback_data='accept')  # кнопка «Да»
        keyboard.add(key_yes)
        bot.send_message(message.chat.id, 'https://teletype.in/@sellwell/r1AkRWraH', reply_markup = keyboard)

    else:
        bot.send_message(message.chat.id, 'Привет, {0}'.format(key))


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'accept':
        bot.register_next_step_handler(call.message, reg_func)
    else:
        
        bot.send_message(call.message.chat.id, 'Для работы с ботом необходимо принять соглашение')


@bot.message_handler(commands=['help'])
def help_msg(message):
    bot.send_message(message.chat.id, 'Команды:\n/start - начать работу с ботом\n/help - вывод справки')


bot.polling()
