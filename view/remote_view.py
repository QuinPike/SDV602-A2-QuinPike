from view.des_view import DESView
import FreeSimpleGUI as sg

class RemoteView(DESView):

    def __init__(self):

        remote_layout = [
            # Remote datasets
            [sg.Text("Remote Datasets")],
            [
                sg.Combo(
                    values=[],
                    key="-REMOTE-DATASET-",
                    size=(30, 1)
                ),
                sg.Button("Load Remote Dataset"),
                sg.Button("Add Remote Dataset")
            ],
            [
                sg.Button("Refresh Datasets"),
                sg.Button("Upload Dataset")
            ],

            # Data management
            [
                sg.Button("Remove Selected"),
                sg.Button("Clear Data")
            ],

            # Session chat
            [sg.Text("Session Chat")],
            [
                sg.Multiline(
                    size=(50, 10),
                    disabled=True,
                    autoscroll=True,
                    key="-OUTPUT-"
                )
            ],
            [
                sg.Input(
                    size=(40, 1),
                    key="-CHAT-",
                    do_not_clear=True
                ),
                sg.Button("Send", bind_return_key=True)
            ]
        ]

        super().__init__(
            additional_layout=remote_layout,
            window_size=(1100, 900),
            window_title="Remote Mode"
        )

    def update_messages(self, messages):

        formatted = self.format_messages(messages)

        self.window["-OUTPUT-"].update(formatted)

    def clear_input(self):
        self.window["-CHAT-"].update("")

    def format_messages(self, messages):
        output = ""

        for message in messages:
            if isinstance(message, dict):
                username = message["username"]
                text = message["text"]
            else:
                username = message.username
                text = message.text

            output += f"{username}: {text}\n"

        return output