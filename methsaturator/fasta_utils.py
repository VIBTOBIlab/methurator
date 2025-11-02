import os
import urllib.request
import subprocess
from .config import GENOME_URLS
from tqdm import tqdm
from .verbose_utils import vprint
import rich_click as click


class DownloadProgressBar(tqdm):
    def update_to(self, blocks=1, block_size=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(blocks * block_size - self.n)


def get_reference(genome, fasta, output_dir, verbose):
    os.makedirs(output_dir, exist_ok=True)

    if fasta and genome:
        vprint(
            "[yellow]⚠️ Both --fasta and --genome provided. Using the provided fasta file.[/yellow]",
            verbose,
        )

    if fasta:
        if not (fasta.endswith(".fa") or fasta.endswith(".fasta")):
            raise click.UsageError(
                "The fasta file provided must end with .fa or .fasta."
            )
        if not os.path.exists(fasta):
            raise click.UsageError(f"The fasta file '{fasta}' does not exist.")
        return fasta

    url = GENOME_URLS[genome]
    gz_path = os.path.join(output_dir, f"{genome}.fa.gz")
    fasta_path = os.path.join(output_dir, f"{genome}.fa")

    if not os.path.exists(fasta_path):
        vprint(f"⬇️ Downloading reference genome '{genome}'...", verbose)
        with DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc="Downloading"
        ) as t:
            urllib.request.urlretrieve(url, gz_path, reporthook=t.update_to)
        vprint(f"🗜️  Extracting {gz_path}...", verbose)
        subprocess.run(["gunzip", "-f", gz_path], check=True)
        vprint(f"✅ Reference genome ready: {fasta_path}", verbose)
    else:
        vprint(f"✅ Reference genome already exists: {fasta_path}", verbose)

    return fasta_path
