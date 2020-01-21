class Behavior:
    def __init__(self, controller, bot):
        self.bot = bot
        self.ctrl = controller

    def call(self, msg):
        pass

    def handle_msg(self, msg):
        pass


class NormalBehavior(Behavior):
    def __init__(self, controller, bot):
        Behavior.__init__(controller, bot)


class LockedBehavior(Behavior):
    def __init__(self, controller, bot):
        Behavior.__init__(controller, bot)
