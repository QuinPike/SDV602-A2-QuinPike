
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
        self.current_dataset_id = None
        self.last_dataset_ids = set()
        

    def run(self):

        # Display the placeholder chart
        self.placeholder_chart()

        self.refresh_remote_datasets()

        # Load existing chat messages
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

                self.sync_graph()

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
                    self.save_graph_settings(values)

            # Save chart
            if event == "Save Chart":
                self.save_chart()


            if event == "Refresh Datasets":
                self.refresh_remote_datasets()

            if event == "Upload Dataset":
                self.upload_dataset()

            if event == "-REMOTE-DATASET-":
                self.load_remote_dataset(values)

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

        if not selected:
            return

        dataset = self.remote_datasets.get(selected)

        if not dataset:
            return

        self.current_dataset_id = dataset["_id"]

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

        sg.popup("Remote dataset loaded successfully!")

    def save_graph_settings(self, values):

        if not self.current_dataset_id:
            sg.popup_error("Please select a dataset first.")
            return

        settings = {
            "dataset_id": str(self.current_dataset_id),
            "x_axis": values["-X-"],
            "y_axis": values["-Y-"],
            "title": values["-TITLE-"],
            "description": values["-DESCRIPTION-"],
            "chart_type": values["-CHART-TYPE-"]
        }

        self.session_repository.update_graph(
            self.session_id,
            settings
        )

        self.last_graph_settings = settings.copy()

    def sync_graph(self):

        settings = self.session_repository.get_graph(
            self.session_id
        )

        if not settings:
            return

        if settings == self.last_graph_settings:
            return

        # Load the shared dataset
        dataset = self.dataset_repository.get_by_id(
            settings["dataset_id"],
            self.session_id
        )

        if not dataset:
            return

        self.last_graph_settings = settings.copy()

        self.current_dataset_id = dataset["_id"]

        self.visualiser.load_data_from_records(dataset["data"])

        columns = dataset["columns"]

        self.view.window["-X-"].update(
            values=columns,
            value=settings["x_axis"]
        )

        self.view.window["-Y-"].update(
            values=columns,
            value=settings["y_axis"]
        )

        self.refresh_table()

        # Update chart controls
        self.view.window["-X-"].update(value=settings["x_axis"])
        self.view.window["-Y-"].update(value=settings["y_axis"])
        self.view.window["-TITLE-"].update(value=settings["title"])
        self.view.window["-DESCRIPTION-"].update(value=settings["description"])

        # Regenerate graph
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

        