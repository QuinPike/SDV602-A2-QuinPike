from controller.des_controller import DESController
from view.remote_view import RemoteView
import config
import FreeSimpleGUI as sg

import multiprocessing
from queue import Empty
from controller.remote_worker import remote_worker


class RemoteController(DESController):

    def __init__(self, username, session_id):

        super().__init__(RemoteView())

        self.username = username
        self.session_id = session_id
        self.last_graph_settings = None

        self.remote_datasets = {}
        self.last_dataset_ids = set()
        self.current_version = -1

        self.process_context = multiprocessing.get_context("spawn")

        self.request_queue = None
        self.result_queue = None
        self.worker_process = None

        self.next_request_id = 0
        self.pending_requests = {}
        


    def run(self):

        self.placeholder_chart()
        self.start_worker()

        try:

            self.refresh_remote_datasets()
            self.sync_session(force=True)
            self.send_worker_request("GET_MESSAGES")

            while True:

                event, values = self.view.read(
                    timeout=config.POLL_RATE
                )

                if event == sg.WIN_CLOSED:
                    break

                # Process responses from the worker.
                for result in self.process_worker_results():
                    self.handle_worker_result(result)

                # Periodically synchronise remote data.
                if event == "__TIMEOUT__":

                    self.sync_session()
                    self.refresh_remote_datasets()
                    self.send_worker_request("GET_MESSAGES")

                elif event == "Send":

                    message = values["-CHAT-"].strip()

                    if message:
                        self.send_worker_request(
                            "SEND_MESSAGE",
                            {"text": message}
                        )

                elif event == "Generate":

                    self.generate_chart(values)

                    if self.generated:
                        self.publish_session(values)

                elif event == "Save Chart":
                    self.save_chart()

                elif event == "Refresh Datasets":
                    self.refresh_remote_datasets()

                elif event == "Upload Dataset":
                    self.upload_dataset()

                elif event == "Remove Selected":

                    if self.remove_selected_row(values):
                        self.publish_session()

                elif event == "Clear Data":

                    self.clear_data()
                    self.last_graph_settings = None
                    self.publish_session()

                elif event == "Load Remote Dataset":
                    self.load_remote_dataset(values)

                elif event == "Add Remote Dataset":
                    self.add_remote_dataset(values)

        finally:

            self.stop_worker()
            self.view.close()


    def refresh_remote_datasets(self):

        self.send_worker_request("REFRESH_DATASETS")

    def upload_dataset(self):

        filepath = sg.popup_get_file(
            "Select a CSV file to upload",
            file_types=(("CSV Files", "*.csv"),),
            no_window=True
        )

        if not filepath:
            return

        self.send_worker_request(
            "UPLOAD_DATASET",
            {"filepath": filepath}
        )


    def load_remote_dataset(self, values):

        selected = values.get("-REMOTE-DATASET-")

        if not selected:
            return

        dataset = self.remote_datasets.get(selected)

        if not dataset:
            return

        self.send_worker_request(
            "GET_DATASET",
            {"dataset_id": dataset["id"]},
            context={"operation": "load"}
        )

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

        self.send_worker_request(
            "PUBLISH_SESSION",
            {
                "state": state,
                "expected_version": self.current_version
            },
            context={
                "graph_settings": graph_settings
            }
        )

    def sync_session(self, force=False):

        self.send_worker_request(
            "SYNC_SESSION",
            context={"force": force}
        )

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

        self.send_worker_request(
            "GET_DATASET",
            {"dataset_id": dataset["id"]},
            context={"operation": "add"}
        )

    def start_worker(self):

        self.request_queue = self.process_context.Queue()
        self.result_queue = self.process_context.Queue()

        self.worker_process = self.process_context.Process(
            target=remote_worker,
            args=(
                self.request_queue,
                self.result_queue,
                self.username,
                self.session_id
            )
        )

        self.worker_process.start()


    def send_worker_request(self, action, payload=None, context=None):

        self.next_request_id += 1
        request_id = self.next_request_id

        self.pending_requests[request_id] = context or {}

        self.request_queue.put({
            "request_id": request_id,
            "action": action,
            "payload": payload or {}
        })

        return request_id


    def process_worker_results(self):

        results = []

        while True:

            try:
                result = self.result_queue.get_nowait()
                results.append(result)

            except Empty:
                break

        return results


    def stop_worker(self):

        if self.worker_process is None:
            return

        if self.worker_process.is_alive():

            self.request_queue.put(None)

            self.worker_process.join(timeout=5)

            if self.worker_process.is_alive():
                self.worker_process.terminate()
                self.worker_process.join()

        self.request_queue.close()
        self.result_queue.close()

        self.worker_process = None
        self.request_queue = None
        self.result_queue = None

    def update_remote_datasets(self, datasets):

        dataset_ids = {dataset["id"] for dataset in datasets}

        if dataset_ids == self.last_dataset_ids:
            return

        self.last_dataset_ids = dataset_ids

        self.remote_datasets = {}
        labels = []

        for dataset in datasets:

            label = (
                f'{dataset["filename"]} '
                f'({dataset["id"][-6:]})'
            )

            self.remote_datasets[label] = dataset
            labels.append(label)

        self.view.window["-REMOTE-DATASET-"].update(
            values=labels,
            value=""
        )

    def apply_shared_state(self, state, force=False):

        if not state:
            return

        version = state["version"]

        if not force and version <= self.current_version:
            return

        data = state["data"]
        columns = state["columns"]
        settings = state["graph_settings"]

        if data:
            self.visualiser.load_data_from_records(data)
        else:
            self.clear_data()

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

            self.view.window["-X-"].update(values=[], value="")
            self.view.window["-Y-"].update(values=[], value="")

        self.refresh_table()

        if settings and data:

            self.view.window["-X-"].update(value=settings["x_axis"])
            self.view.window["-Y-"].update(value=settings["y_axis"])
            self.view.window["-TITLE-"].update(value=settings["title"])
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

    def handle_worker_result(self, result):

        request_id = result["request_id"]
        action = result["action"]

        context = self.pending_requests.pop(request_id, {})

        if action == "WORKER_READY":
            print("Remote worker is ready.")
            return

        if action == "WORKER_ERROR":
            sg.popup_error(
                f"Remote worker failed to start: {result.get('error')}"
            )
            return

        if not result["success"]:

            error = result.get("error", "Unknown worker error.")

            if action == "PUBLISH_SESSION" and "SESSION_CONFLICT" in error:

                sg.popup_error(
                    "Another user has updated the session. "
                    "Your changes could not be saved. "
                    "The latest shared data will now be loaded."
                )

                self.sync_session(force=True)

            else:
                sg.popup_error(f"{action} failed: {error}")

            return

        data = result["data"]

        # Refresh dataset dropdown.
        if action == "REFRESH_DATASETS":

            self.update_remote_datasets(data)

        # Dataset upload completed.
        elif action == "UPLOAD_DATASET":

            sg.popup("Dataset uploaded successfully!")
            self.refresh_remote_datasets()

        # Dataset retrieved.
        elif action == "GET_DATASET":

            operation = context.get("operation")

            if operation == "load":

                self.visualiser.load_data_from_records(data["data"])

                columns = data["columns"]

                self.view.window["-X-"].update(
                    values=columns,
                    value=columns[0]
                )

                self.view.window["-Y-"].update(
                    values=columns,
                    value=columns[1] if len(columns) > 1 else columns[0]
                )

                self.refresh_table()
                self.clear_chart()
                self.last_graph_settings = None
                self.publish_session()

                sg.popup("Remote dataset loaded successfully!")

            elif operation == "add":

                if self.visualiser.append_records(data["data"]):

                    self.last_graph_settings = None

                    self.refresh_table()
                    self.clear_chart()
                    self.publish_session()

                    sg.popup("Remote data added successfully.")

                else:
                    sg.popup_error(
                        "Unable to add data. "
                        "Check that the dataset columns match."
                    )

        # Shared session synchronisation.
        elif action == "SYNC_SESSION":

            self.apply_shared_state(
                data,
                force=context.get("force", False)
            )

        # Shared session publishing.
        elif action == "PUBLISH_SESSION":

            self.current_version = data
            self.last_graph_settings = context.get("graph_settings")

        # Retrieve chat messages.
        elif action == "GET_MESSAGES":

            self.view.update_messages(data)

        # Send chat message.
        elif action == "SEND_MESSAGE":

            self.view.clear_input()
            self.send_worker_request("GET_MESSAGES")
