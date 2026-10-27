from view.register_view import RegisterView

import FreeSimpleGUI as sg

class RegisterController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

        self.view = RegisterView()

    def run(self):
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Cancel", "Login"):
                self.view.close()
                return

            if event == "Register":
                try:
                    self.user_repository.create_user(values["-USERNAME-"], values["-PASSWORD-"])
                    self.view.show_message("Registration successful")
                    self.view.close()
                    return
                except Exception as e:
                    self.view.show_error(e)