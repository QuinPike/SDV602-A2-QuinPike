from view.home_view import HomeView
import FreeSimpleGUI as sg
from controller.remote_controller import RemoteController
from controller.login_controller import LoginController
from controller.session_controller import SessionController
from data.user_repository import UserRepository
from data.session_repository import SessionRepository
from controller.local_controller import LocalController


class HomeController:
    def __init__(self):
        self.view = HomeView()
        self.figure_agg = None
        self.user_repository = UserRepository()
        self.session_repository = SessionRepository()

    def run(self):
        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return

            if event == "Local":
                self.view.hide()
                LocalController().run()
                self.view.un_hide()

            if event == "Remote":
                self.view.hide()

                user = LoginController(self.user_repository).run()

                if user:
                    session = SessionController(
                        user,
                        self.session_repository
                    ).run()

                    if session:
                        RemoteController(
                            user.name,
                            session.session_id
                        ).run()

                self.view.un_hide()