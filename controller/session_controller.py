from view.session_view import SessionView
import FreeSimpleGUI as sg


class SessionController:
    def __init__(self, user, session_repository):
        self.user = user
        self.session_repository = session_repository
        self.view = SessionView()

    def run(self):
        while True:
            sessions = self.session_repository.all()
            self.view.update_sessions(sessions)

            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return None

            elif event == "Refresh":
                continue

            elif event == "Create":
                name = values["-SESSION_NAME-"].strip()

                if name:
                    session = self.session_repository.create_session(
                        name,
                        self.user.name
                    )

                    self.view.close()
                    return session
                else:
                    self.view.show_error("Enter a session name.")

            elif event == "Join":
                selected = values["-SESSIONS-"]

                if selected:
                    session = self.session_repository.get_session(
                        selected[0]
                    )

                    if session:
                        self.view.close()
                        return session
                    else:
                        self.view.show_error("Session not found.")
                else:
                    self.view.show_error("Select a session first.")