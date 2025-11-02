import pandas as pd
import os
from .plot_functions import plot_reads_vs_cpgs


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
