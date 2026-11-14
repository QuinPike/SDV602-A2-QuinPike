import matplotlib

matplotlib.use("Agg")

def test_data_visualiser_initialises():
    from model.data_visualiser import DataVisualiser

    visualiser = DataVisualiser()

    assert visualiser is not None