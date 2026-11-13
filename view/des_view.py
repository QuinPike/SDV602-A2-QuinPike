
import FreeSimpleGUI as sg


class DESView:
    def __init__(self, additional_layout=None, window_title="Data Explorer", window_size=(1300, 1000)):

        sg.theme("DarkBlue")

        self.layout = [
            [
                sg.Text("The Data Dashboard", font=("Helvetica", 16, "bold"))
            ]
        ]

        # Add local or remote specific controls
        if additional_layout:
            self.layout.extend(additional_layout)

        # Shared data preview
        self.layout.extend([
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
            [
                sg.Text(
                    "Chart Configuration:",
                    font=("Helvetica", 12, "bold")
                )
            ],

            [
                sg.Text("X Axis:"),
                sg.Combo(
                    values=[],
                    key="-X-",
                    size=(20, 1)
                ),

                sg.Text("Y Axis:"),
                sg.Combo(
                    values=[],
                    key="-Y-",
                    size=(20, 1)
                )
            ],

            [
                sg.Text("Chart Title:"),
                sg.Input(
                    key="-TITLE-",
                    size=(40, 1)
                )
            ],

            [
                sg.Text("Chart Type:"),
                sg.Combo(
                    ["Line", "Bar"],
                    default_value="Line",
                    key="-CHART-TYPE-",
                    readonly=True
                )
            ],
            [sg.Text("Chart Description:")],

            [
                sg.Multiline(
                    key="-DESCRIPTION-",
                    size=(60, 4),
                    expand_x=True
                )
            ],

            [sg.Text("Chart Preview:")],

            # Chart actions
            [
                sg.Button("Generate"),
                sg.Button("Save Chart"),
                sg.Button("Exit")
            ],

            # Matplotlib toolbar and chart
            [
                sg.Canvas(
                    key="-TOOLBAR-",
                    size=(900, 40)
                )
            ],

            [
                sg.Canvas(
                    size=(900, 550),
                    key="-CANVAS-"
                )
            ]
        ])

        self.table_count = 0
        self.current_table_key = None

        self.window = sg.Window(
            window_title,
            self.layout,
            size=window_size,
            resizable=True,
            finalize=True
        )

    def update_table(self, columns, data):

        container = self.window["-TABLE-CONTAINER-"].Widget

        # Remove existing table
        for widget in container.winfo_children():
            widget.destroy()

        self.current_table_key = None

        if not columns:
            return

        self.table_count += 1

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

    def read(self, timeout=None):
        return self.window.read(timeout=timeout)

    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()
