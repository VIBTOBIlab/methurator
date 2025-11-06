import pytest
from unittest.mock import patch, ANY
import gzip
from methsaturator.fasta_utils import get_reference
from methsaturator.config import GENOME_URLS
import pathlib


def test_use_provided_fasta(tmp_path, monkeypatch):
    fasta = pathlib.Path(__file__).parent / "data" / "hg19.fa"
    result = get_reference(
        genome=None,
        fasta=str(fasta),
        output_dir=str(tmp_path),
        verbose=False,
    )

    assert result == str(fasta)


def test_invalid_fasta_extension(tmp_path):
    wrong = tmp_path / "ref.txt"
    wrong.write_text("dummy")

    with pytest.raises(Exception):
        get_reference(
            genome=None,
            fasta=str(wrong),
            output_dir=str(tmp_path),
            verbose=False,
        )


def test_missing_fasta_file(tmp_path):
    missing = tmp_path / "missing.fa"

    with pytest.raises(Exception):
        get_reference(
            genome=None,
            fasta=str(missing),
            output_dir=str(tmp_path),
            verbose=False,
        )


@patch("methsaturator.fasta_utils.subprocess.run")
@patch("methsaturator.fasta_utils.urllib.request.urlretrieve")
def test_download_reference(url_mock, subproc_mock, tmp_path, monkeypatch):
    genome = "hg19"  # pick first available genome
    genome_url = GENOME_URLS[genome]
    url_mock.return_value = None  # no actual download

    # Fake gz file
    gz_file = tmp_path / f"{genome}.fa.gz"
    with gzip.open(gz_file, "wb") as f:
        f.write(b">seq\nATCG\n")

    result = get_reference(
        genome=genome,
        fasta=None,
        output_dir=str(tmp_path),
        verbose=False,
    )

    # Ensure download called correctly
    url_mock.assert_called_once_with(
        genome_url,
        str(gz_file),
        reporthook=ANY,  # ignore progress callback
    )

    # Ensure gunzip executed
    subproc_mock.assert_called_once()
    assert result.endswith(".fa")
