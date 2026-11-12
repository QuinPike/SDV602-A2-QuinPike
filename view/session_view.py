import FreeSimpleGUI as sg


class SessionView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Remote Sessions", font=("Helvetica", 16, "bold"))],

            [sg.Text("Available Sessions")],

            [sg.Listbox(
                values=[],
                size=(45, 10),
                key="-SESSIONS-",
                enable_events=True
            )],

            [sg.Button("Join"), sg.Button("Refresh")],

            [sg.Text("Create a new session")],

            [sg.Input(key="-SESSION_NAME-")],

            [sg.Button("Create"), sg.Button("Cancel")]
        ]

        self.window = sg.Window(
            "Select Session",
            self.layout,
            finalize=True
        )

    def read(self):
        return self.window.read()

    def update_sessions(self, sessions):
        values = [
            f"{session.name} ({session.session_id})"
            for session in sessions
        ]

        self.window["-SESSIONS-"].update(values)

    def close(self):
        self.window.close()

    def show_error(self, message):
        sg.popup_error(message)