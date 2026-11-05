from view.home_view import HomeView
import FreeSimpleGUI as sg
from controller.remote_controller import RemoteController
from controller.login_controller import LoginController
from model.data_visualiser import DataVisualiser
from data.user_repository import UserRepository
from data.message_repository import MessageRepository
from controller.des_controller import DesController

class HomeController:
    def __init__(self):
        self.view = HomeView()
        self.figure_agg = None
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run(self):
        while True: 
            event, values = self.view.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return

            if event == "Local":
                self.view.hide()
                DesController().run()
                self.view.un_hide()

            if event == "Remote":
                self.view.hide()
                user = LoginController(self.user_repository).run()
                if user:
                    RemoteController(user.name, self.message_repository).run()
                else:
                    print(user)
                self.view.un_hide()