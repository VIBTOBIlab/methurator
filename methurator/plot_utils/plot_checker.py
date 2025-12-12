import numpy as np
from methurator.plot_utils.math_model import fit_saturation_model
from methurator.plot_utils.plot_functions import plot_fitted_data, plot_fallback


class PlotObject:
    def __init__(self, output_path):
        self.x_data = []
        self.y_data = []
        self.asymptote = str
        self.params = []
        self.title = str
        self.reads = int
        self.error_msg = None
        self.output_path = output_path


def plot_checker(data, output_path):

    # Create the PlotObject
    plot_obj = PlotObject(output_path)

    # Add the zeros at the beginning of the data to fit the model
    plot_obj.x_data = np.array([0] + data["Percentage"].tolist())
    plot_obj.y_data = np.array([0] + data["CpG_Count"].tolist())

    # try to fit the asymptotic growth model to the data
    fit_result = fit_saturation_model(plot_obj.x_data, plot_obj.y_data)
    fit_success = fit_result["fit_success"]
    plot_obj.params = fit_result["params"]
    plot_obj.asymptote = fit_result["asymptote"]
    plot_obj.error_msg = fit_result["fit_error"]

    # Prepare title and reads information
    plot_obj.title = data["Sample"].iloc[0]
    plot_obj.reads = int(data["Read_Count"].iloc[-1])

    # If fitting was successful, plot the fitted curve;
    # otherwise, plot the dots with the error message
    if fit_success:
        plot_fitted_data(plot_obj)
    else:
        plot_fallback(plot_obj)
