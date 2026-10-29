import FreeSimpleGUI as sg

class ChatView:

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Multiline(size=(50, 20), disabled=True,
                          autoscroll=True, key='-OUTPUT-')],
            [sg.Input(size=(40, 5), key='-CHAT-', do_not_clear=True)],
            [sg.Button('Send', bind_return_key=True)]
        ]

        self.window = sg.Window("Live Chat", self.layout, finalize=True)

    def update_messages(self, text):
        formatted = self.format_messages(text)
        self.window['-OUTPUT-'].update(formatted)

    def clear_input(self):
        self.window['-CHAT-'].update('')

    def read(self, timeout=None):
        return self.window.read(timeout=timeout)

    def close(self):
        self.window.close()

    def show_error(self, message):
        sg.popup_error(message)

    def show_message(self, message):
        sg.popup(message)

    def format_messages(self, messages=[]):
        if messages:
            output = ""
            for message in messages:
                output += f"{message.username}: {message.text}\n"

            return output
