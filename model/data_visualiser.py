from model.file_manager import FileManager
import matplotlib.pyplot as plt
from operator import itemgetter
from bson import ObjectId
from data.database_manager import DatabaseManager
import config

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
            return False

        self.data = data
        return True

    def append_data(self, file_name):
        new = self.__load_csv(file_name)

        if not new or not self.data:
            return False

        if self.data[0].keys() != new[0].keys():
            print("Data doesn't match")
            return False

        self.data.extend(new)
        return True

    def plot_line_chart(self, x_key, y_key, title, series_key=None):
        if not self.data:
            print('No data to plot!')
            return None

        series = {}
        for row in self.data:
            name = row.get(series_key) if series_key else "Data"
            series.setdefault(name, []).append(row)

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

    # Get CSV Columns
    def get_columns(self):
        if not self.data:
            return []

        return list(self.data[0].keys())

    # Get all Records
    def get_data(self):
        return self.data

    def remove_data(self, index):
        if 0 <= index < len(self.data):
            self.data.pop(index)

    def clear_data(self):
        self.data = []

    def save_data(self, file_name):
        return self.file_manager.save_csv(file_name, self.data)

    # Loads data and files from the database
    def load_data_from_records(self, data):
        self.data = data

    def plot_bar_chart(self, x_key, y_key, title="Bar Chart"):
        import matplotlib.pyplot as plt

        if not self.data:
            raise ValueError("No data loaded.")

        # Extract X and Y values
        x_values = [row[x_key] for row in self.data]
        y_values = [float(row[y_key]) for row in self.data]

        # Create the chart
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar(x_values, y_values)

        # Configure chart appearance
        ax.set_title(title)
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)

        # Rotate labels if necessary
        plt.xticks(rotation=45, ha="right")

        fig.tight_layout()

        return fig

    def get_by_id(self, dataset_id, session_id):

        db = DatabaseManager.getInstance()

        collection = db.get_collection(
            config.DATASETS_COLLECTION
        )

        return collection.find_one({
            "_id": ObjectId(dataset_id),
            "session_id": session_id
        })

    def append_records(self, records):
        if not records:
            return False

        if not self.data:
            self.data = records.copy()
            return True

        existing_columns = self.get_columns()
        new_columns = list(records[0].keys())

        if existing_columns != new_columns:
            return False

        self.data.extend(records)
        return True    