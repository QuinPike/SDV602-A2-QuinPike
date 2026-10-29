from data.user_repository import UserRepository
from data.message_repository import MessageRepository
from model.user import User

from controller.login_controller import LoginController
from controller.chat_controller import ChatController

HEADLESS = False

class App:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        login_controller = LoginController(self.user_repository)

        if HEADLESS:
            user = login_controller.login('Bob', 'Password')
            if type(user) == User:
                print('success')
    
        else:
            user = login_controller.run()
            if user:
                ChatController(user.name, self.message_repository).run()
                pass
            else:
                print(user)

if __name__ == "__main__":
    App().run()