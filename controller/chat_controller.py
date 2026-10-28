from view.chat_view import ChatView
import config
import FreeSimpleGUI as sg

class ChatController:
    def __init__(self, username, message_repository):
        self.message_repository = message_repository
        self.username = username

        self.view = ChatView()


    def run(self):

            messages = self.message_repository.all()
            self.view.update_messages(messages)

            while True:
                event, values = self.view.read(timeout=config.POLL_RATE)

                if event == sg.WIN_CLOSED:
                    break

                if event == "__TIMEOUT__":
                    messages = self.message_repository.all()
                    self.view.update_messages(messages)

                if event == "Send":
                    text = values["-CHAT-"]

                    if text:
                        self.message_repository.create_message(self.username, text)
                        self.view.clear_input()
                        messages = self.message_repository.all()
                        self.view.update_messages(messages)

            self.view.close()
