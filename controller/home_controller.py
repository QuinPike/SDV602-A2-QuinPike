from view.home_view import HomeView
import FreeSimpleGUI as sg
from controller.chat_controller import ChatController
from controller.login_controller import LoginController
from data_visualiser import DataVisualiser

# Import the Tkinter canvas bridge from matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HomeController:
    def __init__(self):
        self.view = HomeView()
        # Track the active figure so we can clear/overwrite it cleanly
        self.figure_agg = None 

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
                
                # Make sure these match the actual headers in your 'bd-natural-increase.csv'
                visualiser.load_data('data/bd-natural-increase-2010-2014.csv') 
                
                fig = visualiser.plot_line_chart(
                    x_key='Period',     # Update this to match your real CSV headers
                    y_key='Count',      # Update this to match your real CSV headers
                    title='Natural Increase Trends', 
                    series_key='Region' # Update this to match your real CSV headers
                )
                
                if fig:
                    # 1. Clear out the previous graph if one is already showing
                    if self.figure_agg:
                        self.figure_agg.get_tk_widget().forget()
                        
                    # 2. Get the Tkinter Canvas element via your View window instance
                    # (Assumes HomeView exposes the FreeSimpleGUI window object as self.view.window)
                    canvas_element = self.view.window['-CANVAS-'].TKCanvas
                    
                    # 3. Draw the new plot onto the view's canvas
                    self.figure_agg = self._draw_figure(canvas_element, fig)
                else:
                    sg.popup_error('Failed to load data or generate chart.')

            if event == "Remote":
                user = LoginController(self).run()
                if user:
                    ChatController(user.name, self.message_repository).run()
                else:
                    print(user)
