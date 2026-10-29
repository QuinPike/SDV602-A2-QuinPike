from view.chat_view import ChatView
import config
from view.home_view import HomeView
import FreeSimpleGUI as sg


class HomeController:
    def __init__(self):
        self.view = HomeView()

    def run(self):
        while True: 
            event, values = self.view.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return
