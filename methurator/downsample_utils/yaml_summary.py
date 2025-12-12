import os
import yaml
import importlib.metadata
import numpy as np
import pandas as pd
from datetime import datetime
from methurator.plot_utils.math_model import asymptotic_growth, fit_saturation_model


def _represent_compact_list(dumper, data):
    """Custom YAML representer that uses flow style for short data lists."""
    # Use flow style for data point lists (4 elements with simple types)
    if len(data) in (2, 3, 4) and all(
        isinstance(x, (int, float, bool, type(None))) for x in data
    ):
        return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=True)
    return dumper.represent_sequence("tag:yaml.org,2002:seq", data, flow_style=False)


def build_saturation_analysis(reads_df, cpgs_df):
    """Build saturation analysis data for each sample/coverage combination.

    Uses the same curve fitting logic as the plotting code.
    Returns a list of dicts with saturation analysis per sample, with a list
    of coverage entries keyed by minimum_coverage value.
    """
    # Merge reads and cpgs data
    data = pd.merge(cpgs_df, reads_df, on=["Sample", "Percentage"])

    saturation_data = []

    for sample in data["Sample"].unique():
        sample_data = data[data["Sample"] == sample]
        coverage_list = []

        for coverage in sample_data["Coverage"].unique():
            subset = sample_data[sample_data["Coverage"] == coverage].sort_values(
                by="Percentage"
            )

            # Prepare data for curve fitting (add zero point, same as plot_checker)
            x_data = np.array([0] + subset["Percentage"].tolist())
            y_data = np.array([0] + subset["CpG_Count"].tolist())

            # Fit the model using shared function
            fit_result = fit_saturation_model(x_data, y_data)

            # Build the data points list
            # Format: [percentage, cpg_count, saturation_%, is_predicted]
            data_points = []

            if fit_result["fit_success"]:
                beta0, beta1 = fit_result["params"]
                asymptote = fit_result["asymptote"]

                # Add observed data points
                for x, y in zip(x_data, y_data):
                    saturation_pct = float(round((y / asymptote) * 100, 1))
                    data_points.append([float(x), int(y), saturation_pct, False])

                # Add predicted data points (same x values as plot_functions.py)
                predicted_x = np.linspace(1.2, 2.0, 5)
                predicted_y = asymptotic_growth(predicted_x, beta0, beta1)
                for x, y in zip(predicted_x, predicted_y):
                    saturation_pct = float(round((y / asymptote) * 100, 1))
                    data_points.append([float(x), int(round(y)), saturation_pct, True])

                coverage_entry = {
                    "minimum_coverage": int(coverage),
                    "fit_success": True,
                    "beta0": float(beta0),
                    "beta1": float(beta1),
                    "asymptote": int(round(asymptote)),
                    "data": data_points,
                }
            else:
                # Add observed data points without saturation percentage
                for x, y in zip(x_data, y_data):
                    data_points.append([float(x), int(y), None, False])

                coverage_entry = {
                    "minimum_coverage": int(coverage),
                    "fit_success": False,
                    "fit_error": fit_result["fit_error"],
                    "data": data_points,
                }

            coverage_list.append(coverage_entry)

        saturation_data.append({sample: coverage_list})

    return saturation_data


def generate_yaml_summary(reads_df, cpgs_df, configs, bam_files):
    """Generate a YAML summary file containing all results and metadata."""
    # Build the reads summary data structure, grouped by sample
    # Format: [{sample_name: [[percentage, read_count], ...]}, ...]
    reads_by_sample = {}
    for _, row in reads_df.iterrows():
        sample = row["Sample"]
        if sample not in reads_by_sample:
            reads_by_sample[sample] = []
        reads_by_sample[sample].append(
            [float(row["Percentage"]), int(row["Read_Count"])]
        )
    reads_data = [{sample: data} for sample, data in reads_by_sample.items()]

    # Build the CpGs summary data structure, grouped by sample and coverage
    # Format: [{sample_name: [{minimum_coverage: X, data: [[percentage, cpg_count], ...]}, ...]}, ...]
    cpgs_by_sample = {}
    for _, row in cpgs_df.iterrows():
        sample = row["Sample"]
        coverage = int(row["Coverage"])
        if sample not in cpgs_by_sample:
            cpgs_by_sample[sample] = {}
        if coverage not in cpgs_by_sample[sample]:
            cpgs_by_sample[sample][coverage] = []
        cpgs_by_sample[sample][coverage].append(
            [float(row["Percentage"]), int(row["CpG_Count"])]
        )
    # Convert to list format with minimum_coverage field
    cpgs_data = []
    for sample, coverages in cpgs_by_sample.items():
        coverage_list = []
        for coverage, data in coverages.items():
            coverage_list.append({"minimum_coverage": coverage, "data": data})
        cpgs_data.append({sample: coverage_list})

    # Build the command and options
    command_options = {
        "bam_files": [str(bam) for bam in bam_files],
        "outdir": str(configs.outdir),
        "fasta": str(configs.fasta) if configs.fasta else None,
        "genome": configs.genome,
        "downsampling_percentages": configs.percentages,
        "minimum_coverage": configs.min_covs,
        "rrbs": configs.rrbs,
        "threads": configs.threads,
        "keep_temporary_files": configs.keep_temporary_files,
    }

    # Build saturation analysis
    saturation_analysis = build_saturation_analysis(reads_df, cpgs_df)

    # Build the full YAML structure
    yaml_data = {
        "methurator_summary": {
            "metadata": {
                "date_generated": datetime.now().isoformat(),
                "methurator_version": importlib.metadata.version("methurator"),
                "command": "methurator downsample",
                "options": command_options,
            },
            "reads_summary": reads_data,
            "cpgs_summary": cpgs_data,
            "saturation_analysis": saturation_analysis,
        }
    }

    # Write to YAML file with compact list formatting
    yaml_path = os.path.join(configs.outdir, "methurator_summary.yml")
    yaml.add_representer(list, _represent_compact_list)
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

    return yaml_path
