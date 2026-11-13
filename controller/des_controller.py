
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from model.data_visualiser import DataVisualiser


class DESController:
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

        # Remove the previous toolbar widgets
        toolbar_canvas = self.view.window["-TOOLBAR-"].TKCanvas

        for widget in toolbar_canvas.winfo_children():
            widget.destroy()

        # Create the navigation toolbar
        self.toolbar = NavigationToolbar2Tk(
            figure_canvas_agg,
            toolbar_canvas,
            pack_toolbar=False
        )

        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")

        return figure_canvas_agg

    def generate_chart(self, values):
        x_key = values["-X-"]
        y_key = values["-Y-"]
        title = values["-TITLE-"]
        description = values["-DESCRIPTION-"]
        chart_type = values["-CHART-TYPE-"]

        if not self.visualiser.data:
            sg.popup_error("Please load data first.")
            return

        if not x_key or not y_key:
            sg.popup_error("Please select both axes.")
            return

        try:
            # Generate the selected chart type
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
                sg.popup_error("Please select a valid chart type.")
                return

            if fig is None:
                sg.popup_error("Failed to generate chart.")
                return

            # Add the description
            fig.text(
                0.5, 0.02,
                description,
                ha="center",
                fontsize=9,
                wrap=True
            )

            # Remove the previous chart
            if self.figure_agg is not None:
                self.figure_agg.get_tk_widget().destroy()

            canvas_element = self.view.window["-CANVAS-"].TKCanvas

            self.figure_agg = self._draw_figure(canvas_element, fig)

            self.generated = True
            self.title = title

        except (ValueError, KeyError) as e:
            sg.popup_error(f"Unable to generate chart: {e}")

    def save_chart(self):
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
        columns = self.visualiser.get_columns()
        data = self.visualiser.get_data()

        table_data = [
            [row[column] for column in columns]
            for row in data
        ]

        self.view.update_table(columns, table_data)

    def clear_chart(self):
        if self.figure_agg is not None:
            self.figure_agg.get_tk_widget().destroy()
            self.figure_agg = None

        if self.toolbar is not None:
            self.toolbar.destroy()
            self.toolbar = None

        self.generated = False
        self.placeholder_chart()

    def placeholder_chart(self):
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

        if not self.visualiser.data:
            sg.popup_error(
                "Load your first dataset before adding another."
            )
            return False

        if self.visualiser.append_data(file_path):

            self.refresh_table()
            self.clear_chart()

            return True

        else:
            sg.popup_error(
                "Unable to add data. Check that the CSV columns match."
            )

            return False

    def remove_selected_row(self, values):

        selected = values.get(self.view.current_table_key, [])

        if not selected:
            sg.popup_error("Please select a row.")
            return False

        self.visualiser.remove_data(selected[0])

        self.refresh_table()
        self.clear_chart()

        return True

    def clear_data(self):

        self.visualiser.clear_data()

        self.refresh_table()
        self.clear_chart()

        self.view.window["-X-"].update(values=[])
        self.view.window["-Y-"].update(values=[])