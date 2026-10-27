import sys

import FreeSimpleGUI as sg

sys.dont_write_bytecode = True

from data.user_repository import UserRepository

class LoginView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Username"), sg.InputText(key="-USERNAME-")],
            [sg.Text("Password"), sg.InputText(password_char="*", key="-PASSWORD-")],
            [sg.Button("Login", bind_return_key=True), sg.Button("Cancel")],
            [sg.Text("Don't have an account? "), sg.Text("Register", text_color="blue", enable_events=True)],
        ]

        self.window = sg.Window("Login", self.layout)


    def read(self):
        return self.window.read()
    
    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()

    def show_error(self, message):
        sg.popup_error(message)

    def show_message(self, message):
        sg.popup(message)