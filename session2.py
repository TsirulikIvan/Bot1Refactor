from handler import Handler


class Session:
    def __init__(self, bd_ctrl):
        self.handler = Handler()
        self.ctrl = bd_ctrl

    def auth_func(self, message):
        key = self.ctrl.query('chat_id', msg.from_user.id)
        if key is None:
            self.reg_func(msg)
        else:

    def handle(self, message):
        self.handler.handle(message)
