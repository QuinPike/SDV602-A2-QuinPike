import queue
import pytest

from controller.remote_controller import RemoteController
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class DummyView:
    def __init__(self):
        self.window = {}
        self.current_table_key = "-TABLE-"

    def update_table(self, columns, data):
        pass

    def update_messages(self, messages):
        pass

    def clear_input(self):
        pass

@pytest.fixture
def controller():

    controller = RemoteController(
        username="test_user",
        session_id="test_session",
        view=DummyView()
    )

    yield controller

    plt.close("all")

def test_send_worker_request(controller):
    """Testing the send worker request for multiprocessing"""

    controller.request_queue = queue.Queue()

    request_id = controller.send_worker_request(
        "GET_MESSAGES"
    )

    request = controller.request_queue.get_nowait()

    assert request_id == 1
    assert request["action"] == "GET_MESSAGES"
    assert request["payload"] == {}


def test_worker_request_ids_increment(controller):
    """Test the worker request IDs increment"""
    controller.request_queue = queue.Queue()

    first = controller.send_worker_request("GET_MESSAGES")
    second = controller.send_worker_request("REFRESH_DATASETS")

    assert first == 1
    assert second == 2


def test_worker_request_context(controller):
    """Test if the request context is stored"""
    controller.request_queue = queue.Queue()

    request_id = controller.send_worker_request(
        "GET_DATASET",
        {"dataset_id": "123"},
        context={"operation": "load"}
    )

    assert controller.pending_requests[request_id] == {
        "operation": "load"
    }

def test_process_empty_worker_results(controller):
    """Testing empty worker results"""

    controller.result_queue = queue.Queue()

    results = controller.process_worker_results()

    assert results == []


def test_publish_session_data(controller):
    """Test to check if the session data gets properly published"""
    controller.request_queue = queue.Queue()

    controller.visualiser.load_data_from_records([
        {"Month": "January", "Sales": 100},
        {"Month": "February", "Sales": 150}
    ])

    controller.current_version = 2

    controller.last_graph_settings = {
        "x_axis": "Month",
        "y_axis": "Sales",
        "title": "Monthly Sales",
        "description": "Sales per month",
        "chart_type": "Line"
    }

    controller.publish_session()

    request = controller.request_queue.get_nowait()

    state = request["payload"]["state"]

    assert state["columns"] == ["Month", "Sales"]
    assert len(state["data"]) == 2
    assert state["graph_settings"]["title"] == "Monthly Sales"
    assert request["payload"]["expected_version"] == 2

def test_process_worker_results(controller):
    """Test retrieving worker results."""

    controller.result_queue = queue.Queue()

    controller.result_queue.put({
        "request_id": 1,
        "action": "GET_MESSAGES",
        "success": True,
        "data": []
    })

    results = controller.process_worker_results()

    assert len(results) == 1
    assert results[0]["action"] == "GET_MESSAGES"