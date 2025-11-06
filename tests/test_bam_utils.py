import pytest
from methsaturator.bam_utils import ensure_coordinated_sorted
import pathlib


@pytest.fixture
def bam_file(tmp_path):
    """Create a small test BAM file with pysam."""
    bam_path = pathlib.Path(__file__).parent / "data" / "Ecoli.unsorted.bam"
    return str(bam_path)


def test_file_not_found():
    with pytest.raises(Exception):
        ensure_coordinated_sorted("does_not_exist.bam", verbose=False)


def test_wrong_extension(bam_file):
    wrong = bam_file.replace(".bam", ".txt")
    with pytest.raises(Exception):
        ensure_coordinated_sorted(wrong, verbose=False)


def test_unsorted_bam_triggers_sort(monkeypatch, bam_file):
    calls = []

    def fake_run(*args, **kwargs):
        calls.append(args[0])

    monkeypatch.setattr("subprocess.run", fake_run)

    result = ensure_coordinated_sorted(bam_file, False)

    assert calls, "samtools not called for unsorted BAM"
    assert result.endswith(".csorted.bam")
