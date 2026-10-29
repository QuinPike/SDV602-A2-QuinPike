import FreeSimpleGUI as sg

class HomeView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Button("Local", bind_return_key=True)],
            [sg.Button('Remote', bind_return_key=True)]
        ]
 
        self.window = sg.Window("Home", self.layout)
