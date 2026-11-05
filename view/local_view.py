import FreeSimpleGUI as sg

class LocalView:

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text('The Data Dashboard', font=('Helvetica', 16, 'bold'))],

            [sg.Text("CSV File:"), sg.Input(key="-FILE-", disabled=True),
            sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],

            [sg.Text("X Axis:"), sg.Combo([], key="-X-", size=(20, 1))],
            [sg.Text("Y Axis:"), sg.Combo([], key="-Y-", size=(20, 1))],

            [sg.Text("Chart Title:"), sg.Input(key="-TITLE-")],

            [sg.Canvas(size=(600, 400), key="-CANVAS-")],

            [sg.Button("Load Data"), sg.Button("Generate"), sg.Button('Save Chart'),
            sg.Button("Exit")]   
        ]

        self.window = sg.Window("Local Mode", self.layout, size=(1000, 800))

    def read(self):
        return self.window.read()
    
    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()