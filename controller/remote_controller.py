
from controller.des_controller import DESController
from view.remote_view import RemoteView
import config
import FreeSimpleGUI as sg


class RemoteController(DESController):

    def __init__(self, username, session_id, message_repository):

        super().__init__(RemoteView())

        self.username = username
        self.session_id = session_id
        self.message_repository = message_repository

    def run(self):

        # Display the placeholder chart
        self.placeholder_chart()

        # Load existing chat messages
        messages = self.message_repository.all(self.session_id)
        self.view.update_messages(messages)

        while True:

            event, values = self.view.read(
                timeout=config.POLL_RATE
            )

            if event == sg.WIN_CLOSED:
                break

            # Refresh chat messages
            elif event == "__TIMEOUT__":

                messages = self.message_repository.all(
                    self.session_id
                )

                self.view.update_messages(messages)

            # Send chat message
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

            # Generate chart
            elif event == "Generate":
                self.generate_chart(values)

            # Save chart
            elif event == "Save Chart":
                self.save_chart()

        self.view.close()
