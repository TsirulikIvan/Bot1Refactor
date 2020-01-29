from telebot import types
import bot_behavior as bh
#https://teletype.in/@sellwell/H1NiudZhH

class Session:
    def __init__(self, msg, controller, bot):
        self.in_competition = False
        self.ready = False
        self.behavior = bh.LockedBehavior(bot)
        self.__id = msg.from_user.id
        self.bot = bot
        self.ctrl = controller
        self.checked_reg_func(msg)

    def handle(self, msg):
        self.behavior.handle_msg(msg)

    def checked_reg_func(self, msg):
        key = self.ctrl.query_any_rows('chat_id', msg.from_user.id)
        if key is None:
            self.reg_func(msg)
        else:
            self.behavior = bh.NormalBehavior(self.bot)
            titles = ['Хочу провести переговоры', 'Переговоры по промокоду', 'Тест "Переговорные стили"',
                      'Тест "Когнитивная регуляция эмоций"', 'Статистика по промокоду']
            callbacks = ['start_search', 'code_competition', 'test1', 'test2', 'stat']
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            buttons = [types.InlineKeyboardButton(text=title, callback_data=callback_data)
                       for title, callback_data in zip(titles, callbacks)]
            keyboard.add(*buttons)
            self.bot.send_message(msg.chat.id,
                                  'Здравствуй, {0}'.format(key), reply_markup=keyboard)

            @self.bot.message_handler(content_types=['text'])
            def handler(message):
                print(message)
                self.behavior.handle_msg(message)

            @self.bot.callback_query_handler(func=lambda call: True)
            def callback_worker(call):
                print(call.data)
                if call.data == 'start_search':
                    self.ready = True
                    keyboard = types.InlineKeyboardMarkup()
                    keyboard.add(types.InlineKeyboardButton(text='Отменить поиск', callback_data='cancel_search'))
                    self.bot.send_message(call.message.chat.id, 'Идет поиск визави...\n'
                                                                'Это может занять некоторое время,'
                                                                ' рекомендуем не выключать уведомления',
                                          reply_markup=keyboard)
                elif call.data == 'cancel_search':
                    self.ready = False
                    self.bot.send_message(call.message.chat.id, 'Поиск отменен... \n'
                                                                'Введите /start для отображения функций бота')

    def reg_func(self, message):
        data = [message.from_user.id]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Принять соглашение', callback_data='accept'))
        self.bot.send_message(message.chat.id, 'https://teletype.in/@sellwell/r1AkRWraH', reply_markup=keyboard)

        @self.bot.message_handler(content_types=['text'])
        def handler(message):
            print(message)
            self.behavior.handle_msg(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            print(call.message)
            if call.data == 'accept':
                self.bot.send_message(call.message.chat.id, 'Отлично! Приступим к регистрации.\nВведите ваше имя')
                self.bot.register_next_step_handler(call.message, get_name)

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
            self.checked_reg_func(message)


if __name__ == "__main__":
    pass
