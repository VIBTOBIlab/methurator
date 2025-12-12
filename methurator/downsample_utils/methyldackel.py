import subprocess
import os
import pandas as pd


def run_methyldackel(bam_path, pct, configs, cpgs_df):

    # Create covs directory to store coverage files
    cov_dir = os.path.join(configs.outdir, "covs")
    os.makedirs(cov_dir, exist_ok=True)

    # Use the BAM filename (without directories) as prefix
    bam_name = os.path.basename(bam_path)
    prefix = os.path.join(cov_dir, os.path.splitext(bam_name)[0])
    cmd = [
        "MethylDackel",
        "extract",
        "-@",
        str(configs.threads),
        "-o",
        str(prefix),
        configs.fasta,
        bam_path,
    ]

    # Add RRBS-specific argument if config.rrbs is True
    if configs.rrbs:
        cmd.append("--keepDupes")

    # Run command
    subprocess.run(cmd)

    # Read the file dumped by MethylDackel
    file = prefix + "_CpG.bedGraph"
    
    # Check if file has data (more than just header)
    try:
        df = pd.read_csv(file, sep="\t", header=None, skiprows=1)
        if df.empty:
            raise pd.errors.EmptyDataError("MethylDackel output file is empty")
    except pd.errors.EmptyDataError:
        print(f"Warning: MethylDackel produced no data for {bam_path}. This may be due to chromosome mismatch with reference genome.")
        print(f"Skipping sample: {os.path.basename(bam_path)}")
        return cpgs_df

    # gzip the file and return the stats
    subprocess.run(["gzip", "-f", f"{prefix}_CpG.bedGraph"])
    sample_name = os.path.basename(bam_path).split(".", 1)[0]
    for min_cov in configs.coverages:
        # Count rows where column 5 + column 6 >= min cov param (0-based indexing in pandas)
        num_cpgs = int(((df[4] + df[5]) >= min_cov).sum())
        cpgs_stats = [sample_name, pct, min_cov, num_cpgs]
        cpgs_df.loc[len(cpgs_df)] = cpgs_stats

    return cpgs_df
