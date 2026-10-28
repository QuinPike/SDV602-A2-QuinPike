from data.user_repository import UserRepository
from data.message_repository import MessageRepository

from controller.login_controller import LoginController
from controller.chat_controller import ChatController

class App:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        user = LoginController(self.user_repository).run()

        if user:
            ChatController(user.name, self.message_repository).run()
            pass
        else:
            print(user)

if __name__ == "__main__":
    App().run()