"""
Script to model and visualize the relationship between sequencing reads and CpG counts
using an asymptotic growth function (arctangent). The script fits the model to downsampling data
and visualizes sequencing saturation across different samples.

Author: Edoardo Giuili
"""

import os
import warnings
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit, OptimizeWarning
from .plot_utils.math_model import asymptotic_growth, find_asymptote
from .plot_utils.plot_functions import plot_data, plot_error_data

# ===============================================================
# Core Functions
# ===============================================================


def plot_reads_vs_cpgs(data, output_path, percentages):
    """Fit the asymptotic model and plot reads vs CpGs."""
    x_data = np.array([0] + percentages)
    y_data = np.array([0] + data["CpG_Count"].tolist())

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", OptimizeWarning)
            params, _ = curve_fit(asymptotic_growth, x_data, y_data, p0=[1, 1])
        asymptote = find_asymptote(params)
        fit_success = True

    except (RuntimeError, OptimizeWarning) as e:
        fit_success = False
        params, asymptote, error_msg = None, None, str(e)
        print(f"⚠️ Curve fitting error: {e}")

    title = data["Sample"].iloc[0]
    reads = int(data["Read_Count"].iloc[-1])

    if fit_success:
        plot_data(x_data, y_data, reads, asymptote, params, output_path, title)
    else:
        plot_error_data(x_data, y_data, reads, output_path, title, error_msg)


def select_sample(cpgs_file, reads_file, percentages, out_dir):
    """Main routine to process each sample and generate plots."""
    data = pd.merge(cpgs_file, reads_file, on=["Sample", "Percentage"])

    for sample in data["Sample"].unique():
        sample_data = data[data["Sample"] == sample]
        for min_val in sample_data["Coverage"].unique():
            subset = sample_data[sample_data["Coverage"] == min_val].sort_values(
                by="Percentage"
            )
            plot_dir = os.path.join(out_dir, "plots")
            os.makedirs(plot_dir, exist_ok=True)
            plot_path = f"{plot_dir}/{sample}_{min_val}x_plot.svg"

            plot_reads_vs_cpgs(subset, plot_path, percentages)
