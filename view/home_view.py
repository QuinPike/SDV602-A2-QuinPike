import FreeSimpleGUI as sg

class HomeView:
    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text('Select a Mode', font=('Helvetica', 16, 'bold'))],
            [sg.Button("Local", bind_return_key=True)],
            [sg.Button('Remote', bind_return_key=True)],

        ]
 
        self.window = sg.Window("Home", self.layout, size=(400, 200))

    def read(self):
        return self.window.read()
    
    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()