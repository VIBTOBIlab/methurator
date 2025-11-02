import os
import glob
import rich_click as click
from .verbose_utils import vprint


def import_bam_files(bam_dir):

    # Check if directory exists
    if not os.path.exists(bam_dir):
        raise click.UsageError(f"Directory does not exist: {bam_dir}")

    if not os.path.isdir(bam_dir):
        raise click.UsageError(f"Path is not a directory: {bam_dir}")

    # Get all BAM files inside directory
    bam_files_all = sorted(glob.glob(os.path.join(bam_dir, "*.bam")))

    # Check if any BAM files were found
    if not bam_files_all:
        raise click.UsageError(f"No BAM files found in directory: {bam_dir}")

    # Remove duplicates (based on filename) and warn
    seen_filenames = set()
    bam_files = []
    for bam in bam_files_all:
        fname = os.path.basename(bam)
        if fname in seen_filenames:
            vprint(
                f"[yellow]⚠️ Warning: Duplicate BAM file found and discarded: {fname}[/yellow].",
                True,
            )
        else:
            seen_filenames.add(fname)
            bam_files.append(bam)

    # bam_files now contains only the BAM files
    return bam_files
