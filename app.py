from data.user_repository import UserRepository
from data.message_repository import MessageRepository

from controller.login_controller import LoginController

class App:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        user = LoginController(self.user_repository).run()

        if user:
            # create chatController
            pass

if __name__ == "__main__":
    App().run()