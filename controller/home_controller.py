from view.home_view import HomeView
import FreeSimpleGUI as sg
from controller.chat_controller import ChatController
from controller.login_controller import LoginController
from model.data_visualiser import DataVisualiser
from data.user_repository import UserRepository
from data.message_repository import MessageRepository
from controller.local_controller import LocalController

# Import the Tkinter canvas bridge from matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HomeController:
    def __init__(self):
        self.view = HomeView()
        self.figure_agg = None
        self.user_repository = UserRepository()
        self.message_repository = MessageRepository()

    def _draw_figure(self, canvas, figure):
        """Bridges a Matplotlib figure onto a FreeSimpleGUI canvas widget."""
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

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
                user = LoginController(self.user_repository).run()
                if user:
                    ChatController(user.name, self.message_repository).run()
                else:
                    print(user)
