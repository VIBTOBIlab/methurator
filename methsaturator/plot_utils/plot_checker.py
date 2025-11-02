import warnings
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
from .math_model import asymptotic_growth, find_asymptote
from .plot_functions import plot_fitted_data, plot_error_data


def plot_checker(data, output_path, percentages):

    # Add the zeros at the beginning of the data to fit the model
    x_data = np.array([0] + data["Percentage"].tolist())
    y_data = np.array([0] + data["CpG_Count"].tolist())

    # try to fit the asymptotic growth model to the data
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", OptimizeWarning)
            params, _ = curve_fit(asymptotic_growth, x_data, y_data, p0=[1, 1])
        asymptote = find_asymptote(params)
        fit_success = True
    # If not enough data points or fitting fails, handle the exception
    except (RuntimeError, OptimizeWarning) as e:
        fit_success = False
        params, asymptote, error_msg = None, None, str(e)

    # Prepare title and reads information
    title = data["Sample"].iloc[0]
    reads = int(data["Read_Count"].iloc[-1])

    # If fitting was successful, plot the fitted curve;
    # otherwise, plot the dots with the error message
    if fit_success:
        plot_fitted_data(x_data, y_data, reads, asymptote, params, output_path, title)
    else:
        plot_error_data(x_data, y_data, reads, output_path, title, error_msg)
