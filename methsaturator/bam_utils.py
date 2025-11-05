import subprocess
import os
import pysam
import rich_click as click
from .verbose_utils import vprint


def ensure_coordinated_sorted(bam_path, verbose):

    # Check if file exists
    if not os.path.exists(bam_path):
        raise click.UsageError(f"The file '{bam_path}' does not exist.")

    # Check if file ends with .bam
    if not bam_path.endswith(".bam"):
        raise click.UsageError("The input file must end with .bam")

    with pysam.AlignmentFile(bam_path, "rb") as bam:
        sort_order = bam.header.get("HD", {}).get("SO", None)

    if sort_order == "coordinate":
        return bam_path

    vprint("🔄 BAM file is not coordinate-sorted. Sorting now...", verbose)
    out = bam_path.replace(".bam", ".csorted.bam")
    cmd = ["samtools", "sort", "-o", out, bam_path]

    # Run samtools
    subprocess.run(cmd)

    return out
