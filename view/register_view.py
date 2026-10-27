import sys

import FreeSimpleGUI as sg

sys.dont_write_bytecode = True


class RegisterView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Username"), sg.InputText(key="-USERNAME-")],
            [sg.Text("Password"), sg.InputText(password_char="*", key="-PASSWORD-")],
            [sg.Text("Confirm Password"), sg.InputText(password_char="*", key="-CONFIRM_PASSWORD-")],
            [sg.Button("Register", bind_return_key=True), sg.Button("Cancel")],
            [sg.Text("Already have an account? "), sg.Text("Login", text_color="blue", enable_events=True)],
        ]

        self.window = sg.Window("Register", self.layout)

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