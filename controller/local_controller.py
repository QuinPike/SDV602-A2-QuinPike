from view.local_view import LocalView
from controller.des_controller import DESController
import FreeSimpleGUI as sg


class LocalController(DESController):

    def __init__(self):
        super().__init__(LocalView())


    def run(self):

        # Display the placeholder chart
        self.placeholder_chart()

        while True:
            event, values = self.view.read()

            if event in (sg.WIN_CLOSED, "Exit"):
                self.view.close()
                return

            # Generate chart (inherited from DESController)
            if event == "Generate":
                self.generate_chart(values)

            # Load local CSV data
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

            # Save chart (inherited from DESController)
            if event == "Save Chart":
                self.save_chart()

            # Add another CSV dataset
            if event == "Add Data":

                file_path = values["-FILE-"]

                if not file_path:
                    sg.popup_error("Please select a CSV file.")
                    continue

                if self.add_data(file_path):
                    sg.popup("Data added successfully.")

            # Remove selected table row
            if event == "Remove Selected":
                self.remove_selected_row(values)

            # Clear all data
            if event == "Clear Data":
                self.visualiser.clear_data()

                self.refresh_table()
                self.clear_chart()

                self.view.window["-X-"].update(values=[])
                self.view.window["-Y-"].update(values=[])

                sg.popup("Data cleared.")

            # Save CSV data
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
