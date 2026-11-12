import FreeSimpleGUI as sg

class LocalView:

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text('The Data Dashboard',
                     font=('Helvetica', 16, 'bold'))],

            # File selection
            [
                sg.Text("CSV File:"),
                sg.Input(key="-FILE-", disabled=True),
                sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))
            ],

            # Data management buttons
            [
                sg.Button("Load Data"),
                sg.Button("Add Data"),
                sg.Button("Remove Selected"),
                sg.Button("Clear Data"),
                sg.Button("Save Data")
            ],

            # Data preview
            [sg.Text("Loaded Data:")],
            [
                sg.Column(
                    [[]],
                    key="-TABLE-CONTAINER-",
                    expand_x=True,
                    expand_y=False
                )
            ],

            # Chart configuration
            [sg.Text("Chart Configuration:",
                     font=('Helvetica', 12, 'bold'))],

            [
                sg.Text("X Axis:"),
                sg.Combo([], key="-X-", size=(20, 1)),

                sg.Text("Y Axis:"),
                sg.Combo([], key="-Y-", size=(20, 1))
            ],

            [
                sg.Text("Chart Title:"),
                sg.Input(key="-TITLE-", size=(40, 1))
            ],

            [sg.Text("Chart Description:")],
            [
                sg.Multiline(
                    key="-DESCRIPTION-",
                    size=(60, 4),
                    expand_x=True
                )
            ],

            # Chart preview
            [sg.Text("Chart Preview:")],

            # Chart actions
            [
                sg.Button("Generate"),
                sg.Button("Save Chart"),
                sg.Button("Exit")
            ],
            
            [sg.Canvas(key="-TOOLBAR-")],
            [sg.Canvas(size=(900, 550), key="-CANVAS-")]

        ]

        self.window = sg.Window(
            "Local Mode",
            self.layout,
            size=(1300, 1000),
            resizable=True,
            finalize=True
        )

    def read(self):
        return self.window.read()

    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()

    def update_table(self, columns, data):

        container = self.window["-TABLE-CONTAINER-"].Widget


        for widget in container.winfo_children():
            widget.destroy()

        if not columns:
            return

        self.table_count = getattr(self, "table_count", 0) + 1

        new_table = sg.Table(
            values=data,
            headings=columns,
            key=f"-DATA-TABLE-{self.table_count}-",
            enable_events=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE,
            auto_size_columns=True,
            num_rows=8,
            expand_x=True
        )

        self.window.extend_layout(
            self.window["-TABLE-CONTAINER-"],
            [[new_table]]
        )

        self.current_table_key = f"-DATA-TABLE-{self.table_count}-"