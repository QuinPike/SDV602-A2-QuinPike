import pytest
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from model.data_visualiser import DataVisualiser


@pytest.fixture
def visualiser():
    """Create a fake data visualiser with data. It will not display a UI"""
    visualiser = DataVisualiser()

    visualiser.load_data_from_records([
        {"Month": "January", "Sales": "100", "Region": "North"},
        {"Month": "February", "Sales": "150", "Region": "North"},
        {"Month": "March", "Sales": "200", "Region": "South"},
        {"Month": "April", "Sales": "250", "Region": "South"}
    ])

    yield visualiser

    plt.close("all")


def test_line_chart_generation(visualiser):
    """Generating a line chart test"""
    figure = visualiser.plot_line_chart(
        "Month", "Sales", "Monthly Sales"
    )

    assert figure is not None
    assert len(figure.axes) == 1
    assert len(figure.axes[0].lines) == 1


def test_bar_chart_generation(visualiser):
    """Generating a bar chart"""
    figure = visualiser.plot_bar_chart(
        "Month", "Sales", "Monthly Sales"
    )

    assert figure is not None
    assert len(figure.axes) == 1
    assert len(figure.axes[0].patches) == 4

def test_line_chart_labels(visualiser):
    """Testing line chart labels"""
    figure = visualiser.plot_line_chart(
        "Month", "Sales", "Monthly Sales"
    )

    axis = figure.axes[0]

    assert axis.get_title() == "Monthly Sales"
    assert axis.get_xlabel() == "Month"
    assert axis.get_ylabel() == "Sales"

def test_bar_chart_labels(visualiser):
    """Testing bar chart labels"""
    figure = visualiser.plot_bar_chart(
        "Month", "Sales", "Monthly Sales"
    )

    axis = figure.axes[0]

    assert axis.get_title() == "Monthly Sales"
    assert axis.get_xlabel() == "Month"
    assert axis.get_ylabel() == "Sales"

def test_line_chart_multiple_series(visualiser):
    """Testing a line chart from multiple sources"""
    figure = visualiser.plot_line_chart(
        "Month",
        "Sales",
        "Sales by Region",
        series_key="Region"
    )

    axis = figure.axes[0]

    assert len(axis.lines) == 2
    assert axis.get_legend() is not None

def test_line_chart_empty_data():
    """Testing empty data with line chart"""
    visualiser = DataVisualiser()

    result = visualiser.plot_line_chart(
        "Month", "Sales", "Empty Chart"
    )

    assert result is None


def test_bar_chart_empty_data():
    """Testing empty data with bar chart"""
    visualiser = DataVisualiser()

    with pytest.raises(ValueError, match="No data loaded"):
        visualiser.plot_bar_chart(
            "Month", "Sales", "Empty Chart"
        )

def test_get_columns(visualiser):
    """Testing the getting columns method to check if that works"""
    assert visualiser.get_columns() == [
        "Month", "Sales", "Region"
    ]


def test_remove_data(visualiser):
    """Testing removing data"""
    visualiser.remove_data(0)

    assert len(visualiser.get_data()) == 3


def test_clear_data(visualiser):
    """Testing clearing data"""
    visualiser.clear_data()

    assert visualiser.get_data() == []


def test_append_records(visualiser):
    """Testing adding new records to data"""
    new_records = [
        {"Month": "May", "Sales": "300", "Region": "North"}
    ]

    result = visualiser.append_records(new_records)

    assert result is True
    assert len(visualiser.get_data()) == 5


def test_append_records_mismatched_columns(visualiser):
    """Testing mismatched columns"""
    new_records = [
        {"Date": "May", "Revenue": "300"}
    ]

    result = visualiser.append_records(new_records)

    assert result is False
    assert len(visualiser.get_data()) == 4

def test_remove_invalid_index(visualiser):
    """Testing removing items but the row is not valid"""
    visualiser.remove_data(10)

    assert len(visualiser.get_data()) == 4

def test_append_empty_records(visualiser):
    """Testing appending with empty data"""
    result = visualiser.append_records([])

    assert result is False
    assert len(visualiser.get_data()) == 4