from file_manager import FileManager
import matplotlib.pyplot as plt
from operator import itemgetter


class DataVisualiser:

    def __init__(self):
        self.file_manager = FileManager()
        self.data = []

    def __load_csv(self, file_name):
        data = self.file_manager.read_csv(file_name)

        if not data:
            print(f"No data loaded from file: {file_name}")
            return []

        return data

    def load_data(self, file_name):
        data = self.__load_csv(file_name)
        if not data:
            return

        self.data = data

    def append_data(self, file_name):
        new = self.__load_csv(file_name)
        if not new or not self.data:
            return

        if self.data[0].keys() != new[0].keys():
            print("Data doesn't match")
            return

        self.data.extend(new)

    def plot_line_chart(self, x_key, y_key, title, series_key=None):
        if not self.data:
            print('No data to plot!')
            return None

        series = {}
        for row in self.data:
            series.setdefault(row.get(series_key), []).append(row)

        # Explicitly create and track the figure object
        fig, ax = plt.subplots(figsize=(8, 6))

        for name, rows in series.items():
            rows.sort(key=itemgetter(x_key))
            x_values = []
            y_values = []
        for row in rows:
            x_values.append(row[x_key])
            y_values.append(float(row[y_key]))

        ax.plot(x_values, y_values, marker='o', label=name)

        if series_key:
            ax.legend()

        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.set_title(title)

        return fig  # Return the figure object to be embedded