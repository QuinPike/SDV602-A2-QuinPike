from view.local_view import LocalView
import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from model.data_visualiser import DataVisualiser

class LocalController:
    def __init__(self):
        self.view = LocalView()
        self.visualiser = DataVisualiser()
        self.figure_agg = None
        self.generated = False
        self.title = ""
        self.toolbar = None

    def _draw_figure(self, canvas, figure):
        """Bridges a Matplotlib figure onto a FreeSimpleGUI canvas widget."""

        # Create the Matplotlib canvas
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()

        figure_canvas_agg.get_tk_widget().pack(
            side='top',
            fill='both',
            expand=1
        )

        # Remove the previous toolbar
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
        self.toolbar.pack(side='top', fill='x')

        return figure_canvas_agg

    def run(self):

        ## Run the placeholder chart to make it not look ugly
        self.placeholder_chart()

        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Exit"):
                self.view.close()
                return

            if event == "Generate":

                x_key = values["-X-"]
                y_key = values["-Y-"]
                title = values["-TITLE-"]
                description = values["-DESCRIPTION-"]

                if not self.visualiser.data:
                    sg.popup_error("Please load data first.")
                    continue

                if not x_key or not y_key:
                    sg.popup_error("Please select both axes.")
                    continue

                try:
                    fig = self.visualiser.plot_line_chart(
                        x_key=x_key,
                        y_key=y_key,
                        title=title
                    )

                    if fig is not None:

                        if self.figure_agg is not None:
                            self.figure_agg.get_tk_widget().destroy()

                        canvas_element = self.view.window["-CANVAS-"].TKCanvas

                        self.figure_agg = self._draw_figure(
                            canvas_element, fig
                        )

                        self.generated = True
                        self.title = title
                        fig.text(
                            0.5, 0.02,
                            description,
                            ha="center",
                            fontsize=9,
                            wrap=True
                        )

                    else:
                        sg.popup_error("Failed to generate chart.")

                except (ValueError, KeyError) as e:
                    sg.popup_error(f"Unable to generate chart: {e}")

            if event == "Load Data":
                file_path = values["-FILE-"]

                if not file_path:
                    sg.popup_error("Please select a CSV file.")
                    continue

                if not self.visualiser.load_data(file_path):
                    sg.popup_error("Unable to load CSV data.")
                    continue

                columns = self.visualiser.get_columns()

                self.view.window["-X-"].update(values=columns)
                self.view.window["-Y-"].update(values=columns)

                self.refresh_table()
                self.clear_chart()

                sg.popup("Data loaded successfully.")

            if event == "Save Chart":
                if self.generated and self.figure_agg is not None:
                    file_path = sg.popup_get_file(
                        "Save Chart",
                        save_as=True,
                        default_extension=".png",
                        file_types=(("PNG Files", "*.png"), ("PDF Files", "*.pdf"))
                    )

                    if file_path:
                        self.figure_agg.figure.savefig(file_path)
                        sg.popup("Chart saved successfully.")

                else:
                    sg.popup_error("There's no chart to save!")

            if event == "Add Data":
                file_path = values["-FILE-"]

                if not file_path:
                    sg.popup_error("Please select a CSV file.")
                    continue

                if not self.visualiser.data:
                    sg.popup_error("Load your first dataset before adding another.")
                    continue

                if self.visualiser.append_data(file_path):
                    self.refresh_table()
                    self.clear_chart()
                    sg.popup("Data added successfully.")
                else:
                    sg.popup_error("Unable to add data. Check that the CSV columnns match.")

            if event == "Remove Selected":
                selected = values.get(self.view.current_table_key, [])

                if not selected:
                    sg.popup_error("Please select a row.")
                    continue

                self.visualiser.remove_data(selected[0])
                self.refresh_table()
                self.clear_chart()

            if event == "Clear Data":
                self.visualiser.clear_data()
                self.refresh_table()
                self.clear_chart()

                self.view.window["-X-"].update(values=[])
                self.view.window["-Y-"].update(values=[])

                sg.popup("Data cleared.")

            if event == "Save Data":
                if not self.visualiser.data:
                    sg.popup_error("There is no data to save.")
                    continue

                file_path = sg.popup_get_file(
                    "Save CSV Data",
                    save_as=True,
                    default_extension=".csv",
                    file_types=(("CSV Files", "*.csv"),)
                )

                if file_path:
                    if self.visualiser.save_data(file_path):
                        sg.popup("Data saved successfully.")
                    else:
                        sg.popup_error("Unable to save data.")

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