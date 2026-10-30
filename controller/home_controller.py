from view.home_view import HomeView
import FreeSimpleGUI as sg
from controller.chat_controller import ChatController
from controller.login_controller import LoginController
from data_visualiser import DataVisualiser
from data.user_repository import UserRepository
from data.message_repository import MessageRepository

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
                visualiser = DataVisualiser()
                
                visualiser.load_data('data/bd-natural-increase-2010-2014.csv') 
                
                fig = visualiser.plot_line_chart(
                    x_key='Period',
                    y_key='Count',
                    title='Natural Increase Trends', 
                    series_key='Region'
                )
                
                if fig:
                    if self.figure_agg:
                        self.figure_agg.get_tk_widget().forget()
        
                    canvas_element = self.view.window['-CANVAS-'].TKCanvas
                    
                    self.figure_agg = self._draw_figure(canvas_element, fig)
                else:
                    sg.popup_error('Failed to load data or generate chart.')

            if event == "Remote":
                user = LoginController(self.user_repository).run()
                if user:
                    ChatController(user.name, self.message_repository).run()
                else:
                    print(user)
