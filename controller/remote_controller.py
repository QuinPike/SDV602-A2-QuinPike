from view.remote_view import RemoteView
import config
import FreeSimpleGUI as sg


class RemoteController:

    def __init__(self, username, session_id, message_repository):

        self.message_repository = message_repository
        self.username = username
        self.session_id = session_id

        self.view = RemoteView()

    def run(self):

        messages = self.message_repository.all(self.session_id)
        self.view.update_messages(messages)

        while True:

            event, values = self.view.read(
                timeout=config.POLL_RATE
            )

            if event == sg.WIN_CLOSED:
                break

            elif event == "__TIMEOUT__":

                messages = self.message_repository.all(
                    self.session_id
                )

                self.view.update_messages(messages)

            elif event == "Send":

                text = values["-CHAT-"].strip()

                if text:

                    self.message_repository.create_message(
                        self.username,
                        text,
                        self.session_id
                    )

                    self.view.clear_input()

                    messages = self.message_repository.all(
                        self.session_id
                    )

                    self.view.update_messages(messages)

        self.view.close()
