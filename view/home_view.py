import FreeSimpleGUI as sg

class HomeView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Button("Local", bind_return_key=True)],
            [sg.Button('Remote', bind_return_key=True)],
            [sg.Text('My Data Dashboard', font=('Helvetica', 16, 'bold'))],
            [sg.Canvas(size=(800, 600), key='-CANVAS-')],  # Reserve space for the chart [1]
            [sg.Button('Load Data & Plot'), sg.Button('Exit')]
        ]
 
        self.window = sg.Window("Home", self.layout, size=(800, 600))

    def read(self):
        return self.window.read()
    
    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()