import os
import glob
import rich_click as click
from methurator.config_utils.verbose_utils import vprint
from methurator.config_utils.validation_utils import ensure_coordinated_sorted


def bam_to_list(configs):

    # Loops over the bam files specified and ensures are csorted
    csorted_bams = []
    for bam_file in configs.bam:
        try:
            csorted_bams.append(ensure_coordinated_sorted(bam_file, configs))
        except ValueError as e:
            raise click.UsageError(f"{e}")
    return csorted_bams


def import_bam_files(bam_dir):

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
