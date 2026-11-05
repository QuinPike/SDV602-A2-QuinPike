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

            if event in (sg.WIN_CLOSED, "Exit"):
                self.view.close()
                return

            if event == "Generate":
                visualiser = DataVisualiser()

                # 1. Retrieve user inputs

                columns = visualiser.get_columns()

                self.view.window["-X-"].update(values=columns)
                self.view.window["-Y-"].update(values=columns)
                file_path = values["-FILE-"]
                x_key = values["-X-"]
                y_key = values["-Y-"]
                title = values["-TITLE-"]

                # 2. Validate inputs
                if not file_path:
                    sg.popup_error("Please select a file.")
                    continue

                if not x_key or not y_key:
                    sg.popup_error("Please select both axes.")
                    continue

                # 3. Load the selected file
                visualiser.load_data(file_path)

                try:
                    # 4. Generate the chart
                    fig = visualiser.plot_line_chart(
                        x_key=x_key,
                        y_key=y_key,
                        title=title
                    )

                    # 5. Display the chart
                    if fig is not None:

                        if self.figure_agg is not None:
                            self.figure_agg.get_tk_widget().destroy()

                        canvas_element = self.view.window["-CANVAS-"].TKCanvas

                        self.figure_agg = self._draw_figure(canvas_element, fig)

                    else:
                        sg.popup_error("Failed to generate chart.")

                except ValueError as e:
                    sg.popup_error(f"Unable to generate chart with selected values: {e}")
                    pass

            if event == "Load Data":
                file_path = values["-FILE-"]

                if not file_path:
                    sg.popup_error("Please select a CSV file.")
                    continue

                visualiser = DataVisualiser()
                visualiser.load_data(file_path)

                columns = visualiser.get_columns()

                if not columns:
                    sg.popup_error("No columns found in CSV.")
                    continue

                self.view.window["-X-"].update(values=columns)
                self.view.window["-Y-"].update(values=columns)

