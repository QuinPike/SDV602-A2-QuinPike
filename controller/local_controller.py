from view.local_view import LocalView
import FreeSimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model.data_visualiser import DataVisualiser

class LocalController:
    def __init__(self):
        self.view = LocalView()
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

            if event == "Generate":
                # Your chart-generation logic goes here.
                visualiser = DataVisualiser()
                print (visualiser)
                pass
