from view.login_view import LoginView
from controller.register_controller import RegisterController
import FreeSimpleGUI as sg

class LoginController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

        self.view = LoginView()

    def run(self):
        
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return

            if event == "Register":
                self.view.hide()
                # Create a register controller and run it
                RegisterController(self.user_repository).run()
                self.view.un_hide()

            if event == "Login":
                user = self.login(values["-USERNAME-"], values["-PASSWORD-"])
                if user:
                    self.view.show_message("Login successful")
                    self.view.close()
                    return user

                self.view.show_error("Login failed")

    def login(self, username, password):
        return self.user_repository.login(username, password)