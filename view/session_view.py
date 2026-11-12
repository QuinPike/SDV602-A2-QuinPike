
import FreeSimpleGUI as sg


class SessionView:
    def __init__(self):
        sg.theme("DarkBlue")
        self.session_map = {}

        self.layout = [
            [sg.Text("Remote Sessions", font=("Helvetica", 16, "bold"))],
            [sg.Text("Available Sessions")],
            [sg.Listbox(
                values=[],
                size=(45, 10),
                key="-SESSIONS-",
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE
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
        self.session_map = {}

        for session in sessions:
            label = f"{session.name} ({session.session_id})"
            self.session_map[label] = session.session_id

        self.window["-SESSIONS-"].update(
            list(self.session_map.keys())
        )

    def get_session_id(self, selected_label):
        return self.session_map.get(selected_label)

    def close(self):
        self.window.close()

    def show_error(self, message):
        sg.popup_error(message)
