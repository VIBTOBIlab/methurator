import subprocess
import os
import yaml
import hashlib
from pathlib import Path


def md5sum(path):
    """Compute md5 checksum of a file."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_date_generated(summary_dict):
    """
    Remove metadata.date_generated from a loaded methurator_summary dict.
    Modifies the dict in place and returns it.
    """
    summary = summary_dict.get("methurator_summary", {})
    metadata = summary.get("metadata", {})
    metadata.pop("date_generated", None)
    options = metadata.get("options", {})
    options.pop("outdir", None)
    return summary_dict


def test_methurator_downsample(tmp_path):
    """Test the 'methurator downsample' CLI command."""

    # Define the command as a list (like in subprocess)
    cmd = [
        "methurator",
        "downsample",
        "tests/data/Ecoli.csorted.bam",
        "--fasta",
        "tests/data/genome.fa",
        "-mc",
        "1,3",
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

    if summary["saturation_analysis"]:
        first_saturation_entry = summary["saturation_analysis"][0]
        assert isinstance(first_saturation_entry, dict)
        sample_name = list(first_saturation_entry.keys())[0]
        assert isinstance(first_saturation_entry[sample_name], list)
        # Corresponds to minimum_coverage == 1
        first_coverage_entry = first_saturation_entry[sample_name][0]
        assert isinstance(first_coverage_entry, dict)
        assert "minimum_coverage" in first_coverage_entry
        assert "fit_success" in first_coverage_entry
        assert "beta0" in first_coverage_entry
        assert "beta1" in first_coverage_entry
        assert "asymptote" in first_coverage_entry
        assert "data" in first_coverage_entry
        # Each data entry should be
        # [downsampling_percentage, reads, saturation, fit_success]
        assert len(first_coverage_entry["data"][0]) == 4

    # Validate with test file
    file_path = Path(__file__).parent / "data/methurator_summary.yml"
    with open(file_path) as f:
        expected_summary_file = yaml.safe_load(f)

    # Remove fields that vary (outdir, date_generated)
    expected_summary_file = strip_date_generated(expected_summary_file)
    yaml_data = strip_date_generated(yaml_data)
    assert yaml_data == expected_summary_file
