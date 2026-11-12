import FreeSimpleGUI as sg
from view.des_view import DESView


class LocalView(DESView):
    def __init__(self):

        # Controls specific to local mode
        local_controls = [

            # CSV file selection
            [
                sg.Text("CSV File:"),
                sg.Input(
                    key="-FILE-",
                    disabled=True
                ),
                sg.FileBrowse(
                    file_types=(("CSV Files", "*.csv"),)
                )
            ],

            # Data management buttons
            [
                sg.Button("Load Data"),
                sg.Button("Add Data"),
                sg.Button("Remove Selected"),
                sg.Button("Clear Data"),
                sg.Button("Save Data"),
                sg.Button("Exit")
            ]
        ]

        # Initialise shared DES interface
        super().__init__(
            window_title="Local Mode",
            window_size=(1300, 1000),
            additional_layout=local_controls
        )