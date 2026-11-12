from view.des_view import DESView
import FreeSimpleGUI as sg

class RemoteView(DESView):
    def __init__(self):

        # Remote-specific controls
        remote_layout = [

            # Remote dataset selection
            [
                sg.Text("Remote Dataset"),

                sg.Combo(
                    values=[],
                    key="-REMOTE-DATASET-",
                    size=(30, 1)
                ),

                sg.Button("Refresh Datasets"),
                sg.Button("Upload Dataset")
            ],

            # Session chat
            [
                sg.Text("Session Chat")
            ],

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

                sg.Button(
                    "Send",
                    bind_return_key=True
                )
            ]
        ]

        # Initialise shared DES interface
        super().__init__(
            additional_layout=remote_layout,
            window_size=(1100, 850),
            window_title="Remote Mode"
        )

    def update_messages(self, messages):

        formatted = self.format_messages(messages)

        self.window["-OUTPUT-"].update(formatted)

    def clear_input(self):
        self.window["-CHAT-"].update("")

    def format_messages(self, messages=None):

        if messages is None:
            messages = []

        output = ""

        for message in messages:
            output += f"{message.username}: {message.text}\n"

        return output
