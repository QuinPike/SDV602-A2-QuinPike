
import pytest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from controller.des_controller import DESController


@pytest.fixture
def controller():
    controller = DESController(None)
    yield controller
    plt.close("all")


@pytest.fixture
def csv_file(tmp_path):
    file_path = tmp_path / "sales.csv"

    file_path.write_text(
        "Month,Sales,Region\n"
        "January,100,North\n"
        "February,150,North\n"
        "March,200,South\n",
        encoding="utf-8"
    )

    return file_path

def test_load_valid_csv(controller, csv_file):

    result = controller.visualiser.load_data(str(csv_file))

    assert result is True
    assert len(controller.visualiser.get_data()) == 3


def test_load_csv_columns(controller, csv_file):

    controller.visualiser.load_data(str(csv_file))

    assert controller.visualiser.get_columns() == [
        "Month", "Sales", "Region"
    ]


def test_load_missing_file(controller, tmp_path):

    file_path = tmp_path / "missing.csv"

    result = controller.visualiser.load_data(str(file_path))

    assert result is False

def test_append_matching_csv(controller, csv_file, tmp_path):

    controller.visualiser.load_data(str(csv_file))

    additional_file = tmp_path / "additional.csv"

    additional_file.write_text(
        "Month,Sales,Region\n"
        "April,250,South\n",
        encoding="utf-8"
    )

    result = controller.append_data(str(additional_file))

    assert result is True
    assert len(controller.visualiser.get_data()) == 4


def test_append_mismatched_csv(controller, csv_file, tmp_path):

    controller.visualiser.load_data(str(csv_file))

    additional_file = tmp_path / "different.csv"

    additional_file.write_text(
        "Month,Profit\n"
        "April,300\n",
        encoding="utf-8"
    )

    with pytest.raises(ValueError):
        controller.append_data(str(additional_file))

    assert len(controller.visualiser.get_data()) == 3


def test_append_without_initial_data(controller, csv_file):

    with pytest.raises(ValueError):
        controller.append_data(str(csv_file))

def test_remove_record(controller, csv_file):

    controller.visualiser.load_data(str(csv_file))

    controller.remove_data(0)

    assert len(controller.visualiser.get_data()) == 2
    assert controller.visualiser.get_data()[0]["Month"] == "February"


def test_remove_invalid_record(controller):

    with pytest.raises(IndexError):
        controller.remove_data(10)


def test_clear_dataset(controller, csv_file):

    controller.visualiser.load_data(str(csv_file))

    controller.clear_dataset()

    assert controller.visualiser.get_data() == []

def test_save_csv(controller, csv_file, tmp_path):

    controller.visualiser.load_data(str(csv_file))

    output_file = tmp_path / "saved_sales.csv"

    result = controller.visualiser.save_data(str(output_file))

    assert result is True
    assert output_file.exists()


def test_reload_saved_csv(controller, csv_file, tmp_path):

    controller.visualiser.load_data(str(csv_file))

    output_file = tmp_path / "saved_sales.csv"

    controller.visualiser.save_data(str(output_file))

    new_controller = DESController(None)

    result = new_controller.visualiser.load_data(str(output_file))

    assert result is True
    assert len(new_controller.visualiser.get_data()) == 3

def test_generate_line_chart_from_local_data(controller, csv_file):

    controller.visualiser.load_data(str(csv_file))

    fig = controller.create_chart(
        "Month", "Sales", "Monthly Sales", "Line"
    )

    assert fig is not None
    assert len(fig.axes[0].lines) == 1


def test_generate_bar_chart_from_local_data(controller, csv_file):

    controller.visualiser.load_data(str(csv_file))

    fig = controller.create_chart(
        "Month", "Sales", "Monthly Sales", "Bar"
    )

    assert fig is not None
    assert len(fig.axes[0].patches) == 3


def test_save_local_chart(controller, csv_file, tmp_path):

    controller.visualiser.load_data(str(csv_file))

    fig = controller.create_chart(
        "Month", "Sales", "Monthly Sales", "Line"
    )

    output_file = tmp_path / "sales_chart.png"

    controller.save_chart_to_file(fig, str(output_file))

    assert output_file.exists()
    assert output_file.stat().st_size > 0
