import subprocess
import os
import pandas as pd


def run_methyldackel(bam_path, pct, fasta, outdir, min_cov, threads):
    # Use the BAM filename (without directories) as prefix
    bam_name = os.path.basename(bam_path)
    cov_dir = os.path.join(outdir, "covs")
    os.makedirs(cov_dir, exist_ok=True)
    prefix = os.path.join(cov_dir, os.path.splitext(bam_name)[0])
    cmd = ["MethylDackel", "extract", "-@", threads, "-o", str(prefix), fasta, bam_path]

    # Run command
    subprocess.run(cmd)

    # Read the file (assuming tab-separated)
    file = prefix + "_CpG.bedGraph"
    df = pd.read_csv(file, sep="\t", header=None, skiprows=1)
    # Count rows where column 5 + column 6 >= 3 (0-based indexing in pandas)
    num_cpgs = int(((df[4] + df[5]) >= min_cov).sum())

    subprocess.run(["gzip", "-f", f"{prefix}_CpG.bedGraph"])
    sample_name = os.path.basename(bam_path).split(".", 1)[0]
    cpgs_stats = [sample_name, pct, min_cov, num_cpgs]
    return cpgs_stats
