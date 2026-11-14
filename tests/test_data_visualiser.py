import pytest
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from model.data_visualiser import DataVisualiser


@pytest.fixture
def visualiser():
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
    figure = visualiser.plot_line_chart(
        "Month", "Sales", "Monthly Sales"
    )

    assert figure is not None
    assert len(figure.axes) == 1
    assert len(figure.axes[0].lines) == 1


def test_bar_chart_generation(visualiser):
    figure = visualiser.plot_bar_chart(
        "Month", "Sales", "Monthly Sales"
    )

    assert figure is not None
    assert len(figure.axes) == 1
    assert len(figure.axes[0].patches) == 4

def test_line_chart_labels(visualiser):
    figure = visualiser.plot_line_chart(
        "Month", "Sales", "Monthly Sales"
    )

    axis = figure.axes[0]

    assert axis.get_title() == "Monthly Sales"
    assert axis.get_xlabel() == "Month"
    assert axis.get_ylabel() == "Sales"

def test_bar_chart_labels(visualiser):
    figure = visualiser.plot_bar_chart(
        "Month", "Sales", "Monthly Sales"
    )

    axis = figure.axes[0]

    assert axis.get_title() == "Monthly Sales"
    assert axis.get_xlabel() == "Month"
    assert axis.get_ylabel() == "Sales"

def test_line_chart_multiple_series(visualiser):
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
    visualiser = DataVisualiser()

    result = visualiser.plot_line_chart(
        "Month", "Sales", "Empty Chart"
    )

    assert result is None


def test_bar_chart_empty_data():
    visualiser = DataVisualiser()

    with pytest.raises(ValueError, match="No data loaded"):
        visualiser.plot_bar_chart(
            "Month", "Sales", "Empty Chart"
        )

def test_get_columns(visualiser):
    assert visualiser.get_columns() == [
        "Month", "Sales", "Region"
    ]


def test_remove_data(visualiser):
    visualiser.remove_data(0)

    assert len(visualiser.get_data()) == 3


def test_clear_data(visualiser):
    visualiser.clear_data()

    assert visualiser.get_data() == []


def test_append_records(visualiser):
    new_records = [
        {"Month": "May", "Sales": "300", "Region": "North"}
    ]

    result = visualiser.append_records(new_records)

    assert result is True
    assert len(visualiser.get_data()) == 5


def test_append_records_mismatched_columns(visualiser):
    new_records = [
        {"Date": "May", "Revenue": "300"}
    ]

    result = visualiser.append_records(new_records)

    assert result is False
    assert len(visualiser.get_data()) == 4

def test_remove_invalid_index(visualiser):
    visualiser.remove_data(10)

    assert len(visualiser.get_data()) == 4

def test_append_empty_records(visualiser):
    result = visualiser.append_records([])

    assert result is False
    assert len(visualiser.get_data()) == 4