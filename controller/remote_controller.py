from controller.des_controller import DESController
from view.remote_view import RemoteView
import config
import FreeSimpleGUI as sg
import csv
import os

from data.dataset_repository import DatasetRepository
from data.session_repository import SessionRepository


class RemoteController(DESController):

    def __init__(self, username, session_id, message_repository):

        super().__init__(RemoteView())

        self.username = username
        self.session_id = session_id
        self.message_repository = message_repository
        self.last_graph_settings = None

        self.dataset_repository = DatasetRepository()
        self.session_repository = SessionRepository()
        self.remote_datasets = {}
        self.last_dataset_ids = set()
        self.current_version = -1
        

    def run(self):

        self.placeholder_chart()

        self.refresh_remote_datasets()

        # Load the current shared session state.
        self.sync_session(force=True)

        messages = self.message_repository.all(self.session_id)
        self.view.update_messages(messages)

        while True:

            event, values = self.view.read(
                timeout=config.POLL_RATE
            )

            if event == sg.WIN_CLOSED:
                break

            # Refresh chat messages
            if event == "__TIMEOUT__":

                self.sync_session()

                self.refresh_remote_datasets()

                messages = self.message_repository.all(
                    self.session_id
                )

                self.view.update_messages(messages)

            # Send chat message
            if event == "Send":

                text = values["-CHAT-"].strip()

                if text:

                    self.message_repository.create_message(
                        self.username,
                        text,
                        self.session_id
                    )

                    self.view.clear_input()

                    messages = self.message_repository.all(
                        self.session_id
                    )

                    self.view.update_messages(messages)

            # Generate chart
            if event == "Generate":

                self.generate_chart(values)

                if self.generated:
                    self.publish_session(values)

            # Save chart
            if event == "Save Chart":
                self.save_chart()


            if event == "Refresh Datasets":
                self.refresh_remote_datasets()

            if event == "Upload Dataset":
                self.upload_dataset()

            if event == "Remove Selected":
                self.remove_selected_row(values)
                self.publish_session()

            if event == "Clear Data":
                self.clear_data()
                self.last_graph_settings = None
                self.publish_session()

            if event == "Load Remote Dataset":
                self.load_remote_dataset(values)

            if event == "Add Remote Dataset":
                self.add_remote_dataset(values)

        self.view.close()

    def refresh_remote_datasets(self):

        datasets = self.dataset_repository.all_for_session(
            self.session_id
        )

        dataset_ids = {str(dataset["_id"]) for dataset in datasets}

        # Only update the dropdown when datasets have changed
        if dataset_ids == self.last_dataset_ids:
            return

        self.last_dataset_ids = dataset_ids

        self.remote_datasets = {}
        labels = []

        for dataset in datasets:

            label = f'{dataset["filename"]} ({str(dataset["_id"])[-6:]})'

            self.remote_datasets[label] = dataset
            labels.append(label)

        self.view.window["-REMOTE-DATASET-"].update(
            values=labels,
            value=""
        )

    def upload_dataset(self):

        filepath = sg.popup_get_file(
            "Select a CSV file to upload",
            file_types=(("CSV Files", "*.csv"),),
            no_window=True
        )

        if not filepath:
            return

        try:

            with open(filepath, "r", newline="", encoding="utf-8-sig") as file:

                reader = csv.DictReader(file)

                columns = reader.fieldnames
                data = list(reader)

            if not columns or not data:
                sg.popup_error("The CSV file is empty or invalid.")
                return

            self.dataset_repository.create_dataset(
                filename=os.path.basename(filepath),
                username=self.username,
                session_id=self.session_id,
                columns=columns,
                data=data
            )

            sg.popup("Dataset uploaded successfully!")

            self.refresh_remote_datasets()

        except Exception as error:

            sg.popup_error(f"Could not upload dataset: {error}")


    def load_remote_dataset(self, values):
        selected = values.get("-REMOTE-DATASET-")
        self.last_graph_settings = None

        if not selected:
            return

        dataset = self.remote_datasets.get(selected)

        if not dataset:
            return

        # Load MongoDB data into DataVisualiser
        self.visualiser.load_data_from_records(
            dataset["data"]
        )

        columns = dataset["columns"]

        # Update chart axis selections
        self.view.window["-X-"].update(
            values=columns,
            value=columns[0]
        )

        self.view.window["-Y-"].update(
            values=columns,
            value=columns[1] if len(columns) > 1 else columns[0]
        )

        # Refresh the data preview
        self.refresh_table()

        self.clear_chart()
        self.last_graph_settings = None
        self.publish_session()

        sg.popup("Remote dataset loaded successfully!")

    def publish_session(self, values=None):

        data = self.visualiser.data
        columns = self.visualiser.get_columns()

        graph_settings = self.last_graph_settings

        if values:
            graph_settings = {
                "x_axis": values["-X-"],
                "y_axis": values["-Y-"],
                "title": values["-TITLE-"],
                "description": values["-DESCRIPTION-"],
                "chart_type": values["-CHART-TYPE-"]
            }

        state = {
            "data": data,
            "columns": columns,
            "graph_settings": graph_settings
        }

        new_version = self.session_repository.update_shared_state(
            self.session_id,
            state,
            self.current_version
        )

        if new_version is None:

            sg.popup_error(
                "Another user has updated the session. "
                "Your changes could not be saved. "
                "The latest shared data will now be loaded."
            )

            self.sync_session(force=True)
            return False

        self.current_version = new_version
        self.last_graph_settings = graph_settings

        return True

    def sync_session(self, force=False):

        state = self.session_repository.get_shared_state(
            self.session_id
        )

        if not state:
            return

        version = state["version"]

        # Don't reload data that we already have.
        if not force and version <= self.current_version:
            return

        data = state["data"]
        columns = state["columns"]
        settings = state["graph_settings"]

        # Load the latest shared data.
        if data:
            self.visualiser.load_data_from_records(data)
        else:
            self.clear_data()

        # Update axis dropdowns.
        if columns:

            self.view.window["-X-"].update(
                values=columns,
                value=columns[0]
            )

            self.view.window["-Y-"].update(
                values=columns,
                value=columns[1] if len(columns) > 1 else columns[0]
            )

        else:

            self.view.window["-X-"].update(
                values=[],
                value=""
            )

            self.view.window["-Y-"].update(
                values=[],
                value=""
            )

        self.refresh_table()

        # Update graph settings and regenerate the chart.
        if settings and data:

            self.view.window["-X-"].update(
                value=settings["x_axis"]
            )

            self.view.window["-Y-"].update(
                value=settings["y_axis"]
            )

            self.view.window["-TITLE-"].update(
                value=settings["title"]
            )

            self.view.window["-DESCRIPTION-"].update(
                value=settings["description"]
            )

            self.view.window["-CHART-TYPE-"].update(
                value=settings["chart_type"]
            )

            self.generate_chart({
                "-X-": settings["x_axis"],
                "-Y-": settings["y_axis"],
                "-TITLE-": settings["title"],
                "-DESCRIPTION-": settings["description"],
                "-CHART-TYPE-": settings["chart_type"]
            })

        else:
            self.clear_chart()

        self.last_graph_settings = settings
        self.current_version = version

    def add_remote_dataset(self, values):
        selected = values.get("-REMOTE-DATASET-")

        if not selected:
            sg.popup_error("Please select a remote dataset.")
            return
        
        
        dataset = self.remote_datasets.get(selected)

        if not dataset:
            sg.popup_error("Remote dataset not found.")
            return

        if not self.visualiser.data:
            sg.popup_error("Load a dataset first.")
            return

        if self.visualiser.append_records(dataset["data"]):

            self.last_graph_settings = None

            self.refresh_table()
            self.clear_chart()
            self.publish_session()

            sg.popup("Remote data added successfully.")
        else:
            sg.popup_error(
                "Unable to add data. Check that the dataset columns match."
            )