
import argparse
import sys

from data.user_repository import UserRepository
from data.message_repository import MessageRepository

from controller.login_controller import LoginController
from controller.home_controller import HomeController
from controller.local_controller import LocalController
from controller.remote_controller import RemoteController
from controller.session_controller import SessionController
from data.session_repository import SessionRepository


class App:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def run_gui(self):
        """Launch the normal application."""
        home_controller = HomeController()
        home_controller.run()

    def run_local(self):
        """Launch local data visualisation."""
        local_controller = LocalController()
        local_controller.run()

    def run_remote(self):
        """Launch remote data mode, starting in login page"""
        login_controller = LoginController(self.user_repository)
        user = login_controller.run()

        if not user:
            return

        session_repository = SessionRepository()

        session_controller = SessionController(
            user,
            session_repository
        )

        session = session_controller.run()

        if not session:
            return

        remote_controller = RemoteController(
            user.name,
            session.session_id
        )

        remote_controller.run()

    @staticmethod
    def run_headless():
        """Run all automated tests without opening the GUI."""
        import pytest
        return pytest.main(["tests", "-v"])

def main():
    parser = argparse.ArgumentParser(
        description="DES Application"
    )

    modes = parser.add_mutually_exclusive_group()

    modes.add_argument(
        "--local",
        action="store_true",
        help="Launch local data visualisation"
    )

    modes.add_argument(
        "--remote",
        action="store_true",
        help="Launch remote application"
    )

    modes.add_argument(
        "--headless",
        action="store_true",
        help="Run automated tests without GUI"
    )

    args = parser.parse_args()

    if args.headless:
        sys.exit(App.run_headless())

    app = App()

    if args.local:
        app.run_local()

    elif args.remote:
        app.run_remote()

    else:
        app.run_gui()


if __name__ == "__main__":
    main()
