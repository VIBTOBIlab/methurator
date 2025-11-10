import pytest
from unittest.mock import patch, ANY
import gzip
from methsaturator.config_utils.fasta_utils import get_reference
from methsaturator.config_utils.config import GENOME_URLS
from methsaturator.config_utils.config import ConfigFormatter


def test_invalid_fasta_extension(tmp_path):
    wrong = tmp_path / "ref.txt"
    wrong.write_text("dummy")
    configs = ConfigFormatter(
        **{
            "fasta": str(wrong),
            "outdir": str(tmp_path),
            "genome": None,
            "verbose": False,
        }
    )
    with pytest.raises(Exception):
        get_reference(configs)


def test_missing_fasta_file(tmp_path):
    missing = tmp_path / "missing.fa"
    configs = ConfigFormatter(
        **{
            "fasta": str(missing),
            "outdir": str(tmp_path),
            "genome": None,
            "verbose": False,
        }
    )
    with pytest.raises(Exception):
        get_reference(configs)


@patch("methsaturator.config_utils.fasta_utils.subprocess.run")
@patch("methsaturator.config_utils.fasta_utils.urllib.request.urlretrieve")
def test_download_reference(url_mock, subproc_mock, tmp_path, monkeypatch):
    genome = "hg19"
    genome_url = GENOME_URLS[genome]
    url_mock.return_value = None  # no actual download

    # Fake gz file
    gz_file = tmp_path / f"{genome}.fa.gz"
    with gzip.open(gz_file, "wb") as f:
        f.write(b">seq\nATCG\n")

    # Simulate genome download
    configs = ConfigFormatter(
        **{"fasta": None, "outdir": str(tmp_path), "genome": genome, "verbose": False}
    )
    result = get_reference(configs)

    # Ensure download called correctly
    url_mock.assert_called_once_with(
        genome_url,
        str(gz_file),
        reporthook=ANY,  # ignore progress callback
    )

    # Ensure gunzip executed
    subproc_mock.assert_called_once()
    assert result.endswith(".fa")
