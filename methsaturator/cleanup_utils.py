import os
import shutil


def clean_up(outdir):
    """Cleans up temporary files generated during the analysis.

    Args:
        outdir (str): The output directory where temporary files are stored.
    """
    shutil.rmtree(os.path.join(outdir, "bams"))
    shutil.rmtree(os.path.join(outdir, "covs"))
