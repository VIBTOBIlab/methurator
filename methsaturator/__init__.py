"""
methsaturator
Package for sequencing saturation analysis of
sequencing methylation data.
"""

__version__ = "0.1.0"

from .bam_utils import ensure_coordinated_sorted
from .fasta_utils import get_reference
from .methyldackel import run_methyldackel
from .subsample_bam import subsample_bam
from .percentage_utils import percentage_checker
from .coverage_utils import mincoverage_checker
from .plot_utils.plot_curve import plot_curve

__all__ = [
    "ensure_coordinated_sorted",
    "get_reference",
    "run_methyldackel",
    "subsample_bam",
    "percentage_checker",
    "mincoverage_checker",
    "plot_curve",
    "__version__",
]
