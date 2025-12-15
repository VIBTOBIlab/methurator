import subprocess
import os
import yaml


def test_methurator_downsample(tmp_path):
    """Test the 'methurator downsample' CLI command."""

    # Define the command as a list (like in subprocess)
    cmd = [
        "methurator",
        "downsample",
        "tests/data/Ecoli.csorted.bam",
        "--fasta",
        "tests/data/genome.fa",
        "--outdir",
        str(tmp_path),
    ]

    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Paths of the expected outputs
    cpgs_summary = os.path.join(tmp_path, "methurator_cpgs_summary.csv")
    reads_summary = os.path.join(tmp_path, "methurator_reads_summary.csv")
    yaml_summary = os.path.join(tmp_path, "methurator_summary.yml")

    # Assert that output files exist
    error_info = f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    assert os.path.exists(cpgs_summary), f"{cpgs_summary} not found{error_info}"
    assert os.path.exists(reads_summary), f"{reads_summary} not found{error_info}"
    assert os.path.exists(yaml_summary), f"{yaml_summary} not found{error_info}"

    # Validate YAML structure
    with open(yaml_summary) as f:
        yaml_data = yaml.safe_load(f)

    assert "methurator_summary" in yaml_data
    summary = yaml_data["methurator_summary"]

    # Check metadata fields
    assert "metadata" in summary
    metadata = summary["metadata"]
    assert "date_generated" in metadata
    assert "methurator_version" in metadata
    assert "command" in metadata
    assert metadata["command"] == "methurator downsample"
    assert "options" in metadata

    # Check options
    options = metadata["options"]
    assert "bam_files" in options
    assert "outdir" in options
    assert "downsampling_percentages" in options
    assert "minimum_coverage" in options
    assert "rrbs" in options
    assert "threads" in options

    # Check data sections
    assert "reads_summary" in summary
    assert "cpgs_summary" in summary
    assert isinstance(summary["reads_summary"], list)
    assert isinstance(summary["cpgs_summary"], list)

    # Validate nested structure (sample -> list of [percentage, value(s)])
    if summary["reads_summary"]:
        first_reads_entry = summary["reads_summary"][0]
        assert isinstance(first_reads_entry, dict)
        sample_name = list(first_reads_entry.keys())[0]
        assert isinstance(first_reads_entry[sample_name], list)
        # Each entry should be [percentage, read_count]
        assert len(first_reads_entry[sample_name][0]) == 2

    if summary["cpgs_summary"]:
        first_cpgs_entry = summary["cpgs_summary"][0]
        assert isinstance(first_cpgs_entry, dict)
        sample_name = list(first_cpgs_entry.keys())[0]
        assert isinstance(first_cpgs_entry[sample_name], list)
        # Each entry should be a dict with minimum_coverage and data keys
        first_coverage_entry = first_cpgs_entry[sample_name][0]
        assert isinstance(first_coverage_entry, dict)
        assert "minimum_coverage" in first_coverage_entry
        assert "data" in first_coverage_entry
        # Each data entry should be [percentage, cpg_count]
        assert len(first_coverage_entry["data"][0]) == 2
