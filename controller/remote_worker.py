
import csv
import os

from data.dataset_repository import DatasetRepository
from data.session_repository import SessionRepository
from data.message_repository import MessageRepository


def remote_worker(request_queue, result_queue, username, session_id):
    """
    Background process for remote database operations.

    The repositories and MongoDB connection are created inside
    this process, not inherited from the GUI process.
    """

    try:
        dataset_repository = DatasetRepository()
        session_repository = SessionRepository()
        message_repository = MessageRepository()

        result_queue.put({
            "request_id": None,
            "action": "WORKER_READY",
            "success": True,
            "data": None
        })

    except Exception as error:

        result_queue.put({
            "request_id": None,
            "action": "WORKER_ERROR",
            "success": False,
            "error": str(error)
        })

        return

    while True:

        request = request_queue.get()

        if request is None:
            break

        request_id = request["request_id"]
        action = request["action"]
        payload = request.get("payload", {})

        try:

            # Retrieve datasets belonging to this session.
            if action == "REFRESH_DATASETS":

                datasets = dataset_repository.all_for_session(
                    session_id
                )

                data = [
                    {
                        "id": str(dataset["_id"]),
                        "filename": dataset["filename"],
                        "columns": dataset["columns"],
                        "uploaded_by": dataset.get("uploaded_by", "")
                    }
                    for dataset in datasets
                ]

            # Retrieve one dataset.
            elif action == "GET_DATASET":

                dataset = dataset_repository.get_by_id(
                    payload["dataset_id"],
                    session_id
                )

                if dataset is None:
                    raise ValueError("Dataset not found.")

                data = {
                    "id": str(dataset["_id"]),
                    "filename": dataset["filename"],
                    "columns": dataset["columns"],
                    "data": dataset["data"]
                }

            # Read and upload a CSV file.
            elif action == "UPLOAD_DATASET":

                filepath = payload["filepath"]

                with open(
                    filepath,
                    "r",
                    newline="",
                    encoding="utf-8-sig"
                ) as file:

                    reader = csv.DictReader(file)

                    columns = reader.fieldnames
                    records = list(reader)

                if not columns or not records:
                    raise ValueError(
                        "The CSV file is empty or invalid."
                    )

                dataset_id = dataset_repository.create_dataset(
                    filename=os.path.basename(filepath),
                    username=username,
                    session_id=session_id,
                    columns=columns,
                    data=records
                )

                data = {
                    "id": str(dataset_id),
                    "filename": os.path.basename(filepath),
                    "columns": columns,
                    "record_count": len(records)
                }

            # Retrieve the shared session state.
            elif action == "SYNC_SESSION":

                data = session_repository.get_shared_state(
                    session_id
                )

            # Publish changes to the shared session.
            elif action == "PUBLISH_SESSION":

                data = session_repository.update_shared_state(
                    session_id,
                    payload["state"],
                    payload["expected_version"]
                )

                if data is None:
                    raise ValueError(
                        "SESSION_CONFLICT: Another user has "
                        "updated the session."
                    )

            # Retrieve session chat messages.
            elif action == "GET_MESSAGES":

                messages = message_repository.all(session_id)

                data = [
                    {
                        "username": message.username,
                        "text": message.text
                    }
                    for message in messages
                ]

            # Send a chat message.
            elif action == "SEND_MESSAGE":

                message_repository.create_message(
                    username,
                    payload["text"],
                    session_id
                )

                data = True

            # Stop the worker.
            elif action == "SHUTDOWN":
                break

            else:
                raise ValueError(
                    f"Unknown worker action: {action}"
                )

            result_queue.put({
                "request_id": request_id,
                "action": action,
                "success": True,
                "data": data
            })

        except Exception as error:

            result_queue.put({
                "request_id": request_id,
                "action": action,
                "success": False,
                "error": str(error)
            })
