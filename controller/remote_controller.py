
from controller.des_controller import DESController
from view.remote_view import RemoteView
import config
import FreeSimpleGUI as sg
import csv
import os
from datetime import datetime, timezone

from data.dataset_repository import DatasetRepository


class RemoteController(DESController):

    def __init__(self, username, session_id, message_repository):

        super().__init__(RemoteView())

        self.username = username
        self.session_id = session_id
        self.message_repository = message_repository

        self.dataset_repository = DatasetRepository()
        self.remote_datasets = {}

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
            elif event == "__TIMEOUT__":

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