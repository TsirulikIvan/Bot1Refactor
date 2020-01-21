from telebot import types
from bot_behavior import Behavior


class Session:
    def __init__(self, msg, controller, bot):
        self.is_reg = False
        self.behavior = Behavior(controller, bot)
        self.__id = msg.from_user.id
        self.bot = bot
        self.ctrl = controller
        self.checked_reg_func(msg)

    def call(self, msg):
        self.behavior.call(msg)

    def checked_reg_func(self, msg):
        if self.is_reg:
            self.bot.send_message(msg.chat.id,
                                  'Привет, {0}'.format(self.ctrl.query('chat_id', msg.from_user.id)))
        else:
            self.reg_func(msg)

    def reg_func(self, message):
        print('log_func')
        key = self.ctrl.query('chat_id', message.from_user.id)
        if key is None:
            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура ge
            key_yes = types.InlineKeyboardButton(text='Принять соглашение', callback_data='accept')  # кнопка «Да»
            keyboard.add(key_yes)
            self.bot.send_message(message.chat.id, 'https://teletype.in/@sellwell/r1AkRWraH', reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == 'accept':
                self.bot.send_message(call.message.chat.id, 'Отлично! Приступим к регистрации.\n Введите ваше имя')
                self.bot.register_next_step_handler(call.message, get_name)

        data = [message.from_user.id]

        @self.bot.message_handler(content_types=['text'])
        def get_name(message):
            print('state 4')
            data.append(message.text)
            self.bot.send_message(message.chat.id, 'Введите вашу фамилию:')
            self.bot.register_next_step_handler(message, get_surname)

        def get_surname(message):
            print('state 5')
            data.append(message.text)
            self.bot.send_message(message.chat.id, 'Введите название вашей компании:')
            self.bot.register_next_step_handler(message, get_company)

        def get_company(message):
            print('state 6')
            data.append(message.text)
            self.bot.send_message(message.chat.id, 'Введите ваш телефон (в формате 8):')
            self.bot.register_next_step_handler(message, get_phone)

        def get_phone(message):
            print('state 7')
            data.append(message.text)
            self.bot.send_message(message.chat.id, 'Регистрация завершена!')
            self.ctrl.add_record(tuple(data))


if __name__ == "__main__":
    pass
