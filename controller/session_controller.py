from view.session_view import SessionView
import FreeSimpleGUI as sg


class SessionController:
    def __init__(self, user, session_repository):
        self.user = user
        self.session_repository = session_repository
        self.view = SessionView()

    def run(self):
        while True:
            public_sessions = self.session_repository.all()

            private_sessions = self.session_repository.user_sessions(
                self.user.name
            )

            sessions = public_sessions + private_sessions

            self.view.update_sessions(sessions)

            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return None

            if event == "Refresh":
                continue

            if event == "Create":
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

            if event == "Join":
                selected = values["-SESSIONS-"]

                if selected:
                    session_id = self.view.get_session_id(selected[0])

                    session = self.session_repository.get_session(session_id)

                    if session:
                        self.session_repository.join_session(
                            session_id, self.user.name
                        )

                        self.view.close()
                        return session
                    else:
                        self.view.show_error("Session not found.")
                else:
                    self.view.show_error("Select a session first.")
