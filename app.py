from data.user_repository import UserRepository
from data.message_repository import MessageRepository
from model.user import User

from controller.login_controller import LoginController
from controller.chat_controller import ChatController

from controller.home_controller import HomeController

HEADLESS = False

class App:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        login_controller = LoginController(self.user_repository)
        home_controller = HomeController()

        if HEADLESS:
            user = login_controller.login('Bob', 'Password')
            if type(user) == User:
                print('success')
        else:

            ## user = login_controller.run()
            ## if user:
            ##    ChatController(user.name, self.message_repository).run()
            ##    pass
            ## else:
            ##    print(user)

            home = home_controller.run()

if __name__ == "__main__":
    App().run()