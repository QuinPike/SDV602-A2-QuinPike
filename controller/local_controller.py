from view.local_view import LocalView
import config
import FreeSimpleGUI as sg


class LocalController:
    def __init__(self):
        self.view = LocalView()

    def run(self):
        while True: 
            event, values = self.view.read()
            if event in (sg.WIN_CLOSED, "Cancel"):
                self.view.close()
                return 
                visualiser = DataVisualiser()
                
            visualiser.load_data('data/bd-natural-increase-2010-2014.csv') 

            fig = visualiser.plot_line_chart(
                x_key='Period',
                y_key='Count',
                title='Natural Increase Trends', 
                series_key='Region'
            )
                
            if fig:
                if self.figure_agg:
                    self.figure_agg.get_tk_widget().forget()
        
                    canvas_element = self.view.window['-CANVAS-'].TKCanvas
                    
                    self.figure_agg = self._draw_figure(canvas_element, fig)
                else:
                    sg.popup_error('Failed to load data or generate chart.')

