import os
import yaml
import importlib.metadata
from datetime import datetime


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

    # Build the CpGs summary data structure, grouped by sample
    # Format: [{sample_name: [[percentage, coverage, cpg_count], ...]}, ...]
    cpgs_by_sample = {}
    for _, row in cpgs_df.iterrows():
        sample = row["Sample"]
        if sample not in cpgs_by_sample:
            cpgs_by_sample[sample] = []
        cpgs_by_sample[sample].append(
            [float(row["Percentage"]), int(row["Coverage"]), int(row["CpG_Count"])]
        )
    cpgs_data = [{sample: data} for sample, data in cpgs_by_sample.items()]

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
        }
    }

    # Write to YAML file
    yaml_path = os.path.join(configs.outdir, "methurator_summary.yml")
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

    return yaml_path
