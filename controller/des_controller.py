
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from model.data_visualiser import DataVisualiser


class DESController:
    """This is the parent class of the Local Controller and the Remote Controller. 
    This class draws the figures into the UI, generates the charts, allows saving of a chart, and much more functionality"""
    def __init__(self, view):
        self.view = view
        self.visualiser = DataVisualiser()

        self.figure_agg = None
        self.generated = False
        self.title = ""
        self.toolbar = None

    def _draw_figure(self, canvas, figure):
        """Display a Matplotlib figure inside the GUI."""

        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()

        figure_canvas_agg.get_tk_widget().pack(
            side="top",
            fill="both",
            expand=1
        )
        toolbar_canvas = self.view.window["-TOOLBAR-"].TKCanvas

        for widget in toolbar_canvas.winfo_children():
            widget.destroy()

        self.toolbar = NavigationToolbar2Tk(
            figure_canvas_agg,
            toolbar_canvas,
            pack_toolbar=False
        )

        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")

        return figure_canvas_agg

    def generate_chart(self, values):
        """Generates the chart inside the GUI, the values are based on the users input"""

        try:
            fig = self.create_chart(
                x_key=values["-X-"],
                y_key=values["-Y-"],
                title=values["-TITLE-"],
                chart_type=values["-CHART-TYPE-"],
                description=values["-DESCRIPTION-"]
            )

            if self.figure_agg is not None:
                self.figure_agg.get_tk_widget().destroy()

            canvas_element = self.view.window["-CANVAS-"].TKCanvas

            self.figure_agg = self._draw_figure(canvas_element, fig)

            self.generated = True
            self.title = values["-TITLE-"]

        except (ValueError, KeyError) as e:
            sg.popup_error(f"Unable to generate chart: {e}")

    def save_chart(self):
        """Save the chart to the local machine"""
        if not self.generated or self.figure_agg is None:
            sg.popup_error("There's no chart to save!")
            return

        file_path = sg.popup_get_file(
            "Save Chart",
            save_as=True,
            default_extension=".png",
            file_types=(("PNG Files", "*.png"), ("PDF Files", "*.pdf"))
        )

        if file_path:
            self.figure_agg.figure.savefig(file_path)
            sg.popup("Chart saved successfully.")

    def refresh_table(self):
        """Refreshes the table so when things get updated, the table updates too"""
        columns = self.visualiser.get_columns()
        data = self.visualiser.get_data()

        table_data = [
            [row[column] for column in columns]
            for row in data
        ]

        self.view.update_table(columns, table_data)

    def clear_chart(self):
        """Clears the chart"""
        if self.figure_agg is not None:
            self.figure_agg.get_tk_widget().destroy()
            self.figure_agg = None

        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None

        self.generated = False
        self.placeholder_chart()

    def placeholder_chart(self):
        """Creates a placeholder chart. This is just to have a chart there ready."""
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.set_title("The Data Explorer")
        ax.text(
            0.5, 0.5,
            "The Chart is Empty. Enter files and load data to start!",
            ha="center",
            va="center",
            transform=ax.transAxes
        )

        ax.set_xticks([])
        ax.set_yticks([])

        canvas_element = self.view.window["-CANVAS-"].TKCanvas

        self.figure_agg = self._draw_figure(canvas_element, fig)

    def add_data(self, file_path):
        """Adding data to the table, it then refreshes the table"""
        try:
            self.append_data(file_path)

            self.refresh_table()
            self.clear_chart()

            return True

        except ValueError as e:
            sg.popup_error(str(e))
            return False

    def remove_selected_row(self, values):
        """Removes a selected row in the table"""
        selected = values.get(self.view.current_table_key, [])

        if not selected:
            sg.popup_error("Please select a row.")
            return False

        try:
            self.remove_data(selected[0])

            self.refresh_table()
            self.clear_chart()

            return True

        except IndexError as e:
            sg.popup_error(str(e))
            return False

    def clear_data(self):
        """Clear all data and refreshes the table"""

        self.clear_dataset()

        self.refresh_table()
        self.clear_chart()

        self.view.window["-X-"].update(values=[])
        self.view.window["-Y-"].update(values=[])

    def create_chart(self, x_key, y_key, title, chart_type, description=""):
        """Create the actual chart based on the users input and values entered. There is also error handling"""

        if not self.visualiser.data:
            raise ValueError("No data loaded.")

        if not x_key or not y_key:
            raise ValueError("Both axes must be selected.")

        if chart_type == "Line":
            fig = self.visualiser.plot_line_chart(
                x_key=x_key,
                y_key=y_key,
                title=title
            )

        elif chart_type == "Bar":
            fig = self.visualiser.plot_bar_chart(
                x_key=x_key,
                y_key=y_key,
                title=title
            )

        else:
            raise ValueError("Invalid chart type.")

        if fig is None:
            raise ValueError("Failed to generate chart.")

        fig.text(
            0.5, 0.02,
            description,
            ha="center",
            fontsize=9,
            wrap=True
        )

        return fig

    def save_chart_to_file(self, figure, file_path):
        """This saves the chart to a chosen file on the users home computer they are using"""

        if figure is None:
            raise ValueError("No chart available to save.")

        if not file_path:
            raise ValueError("No file path provided.")

        figure.savefig(file_path)

        return True

    def append_data(self, file_path):
        """Append data into the file"""

        if not self.visualiser.data:
            raise ValueError(
                "Load your first dataset before adding another."
            )

        if not self.visualiser.append_data(file_path):
            raise ValueError(
                "Unable to add data. Check that the CSV columns match."
            )

        return True

    def remove_data(self, index):
        """Remove data from the file"""

        if not 0 <= index < len(self.visualiser.data):
            raise IndexError("Invalid row selection.")

        self.visualiser.remove_data(index)

        return True


    def clear_dataset(self):
        """Clear the entire dataset"""

        self.visualiser.clear_data()

        return True