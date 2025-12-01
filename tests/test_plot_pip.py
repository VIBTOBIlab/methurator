import subprocess


def test_methurator_plot(tmp_path):
    """Test the 'methurator plot' CLI command."""

    # Define the command as a list (like in subprocess)
    cmd = [
        "methurator",
        "plot",
        "-c",
        "tests/data/cpgs_summary.csv",
        "-r",
        "tests/data/reads_summary.csv",
        "--outdir",
        str(tmp_path),
    ]

    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check that the command succeeded
    assert (
        result.returncode == 0
    ), f"Command failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"

    # Path of expected output
    plot = tmp_path / "plots/SRX1631721_1x_plot.html"

    # Assert that the plot was created
    assert plot.exists(), f"{plot} not found"
