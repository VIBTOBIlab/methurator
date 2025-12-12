import subprocess
import os


def test_methurator_downsample(tmp_path):
    """Test the 'methurator downsample' CLI command."""

    # Define the command as a list (like in subprocess)
    cmd = [
        "methurator",
        "downsample",
        "--bam",
        "tests/data/Ecoli.csorted.bam",
        "--fasta",
        "tests/data/genome.fa",
        "--outdir",
        str(tmp_path),
    ]

    # Run the command
    subprocess.run(cmd, capture_output=True, text=True)

    # Paths of the expected outputs
    cpgs_summary = os.path.join(tmp_path, "methurator_cpgs_summary.csv")
    reads_summary = os.path.join(tmp_path, "methurator_reads_summary.csv")

    # Assert that output files exist
    assert os.path.exists(cpgs_summary), f"{cpgs_summary} not found"
    assert os.path.exists(reads_summary), f"{reads_summary} not found"
