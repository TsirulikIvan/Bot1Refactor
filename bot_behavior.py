from telebot import types


class Behavior:
    def __init__(self, bot):
        self.bot = bot

    def handle_msg(self, msg):
        pass


class NormalBehavior(Behavior):
    def handle_msg(self, msg):
        pass

class LockedBehavior(Behavior):

    def handle_msg(self, msg):
        self.bot.send_message(msg.chat.id, 'Для работы бота, пожалуйста,\n '
                                           'примите соглашение и зарегистрируйтесь')
