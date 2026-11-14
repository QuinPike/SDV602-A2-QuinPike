
import pytest
from controller.des_controller import DESController

class TestView:
    """Simple view object for testing controller logic."""

    current_table_key = "-TABLE-"

    def update_table(self, columns, data):
        self.columns = columns
        self.data = data

@pytest.fixture
def controller():
    view = TestView()
    controller = DESController(view)

    controller.visualiser.load_data_from_records([
        {"Month": "January", "Sales": "100"},
        {"Month": "February", "Sales": "150"}
    ])

    return controller


def test_refresh_table(controller):
    controller.refresh_table()

    assert controller.view.columns == ["Month", "Sales"]

    assert controller.view.data == [
        ["January", "100"],
        ["February", "150"]
    ]

def test_remove_selected_row(controller):
    controller.remove_selected_row = None