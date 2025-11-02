import rich_click as click
from .verbose_utils import vprint


def mincoverage_checker(coverages):
    """
    Converts a comma-separated string into a list of integers.
    """
    values = coverages.split(",")
    list_coverages = []

    for x in values:
        x = x.strip()
        if not x.isdigit():
            raise click.UsageError(
                f"Invalid minimum coverage value: '{x}'. All minimum coverage must be integers."
            )
        if int(x) == 0:
            vprint(
                f"[yellow]⚠️ Warning: coverage values must be at least >=1, '{x}' was ignored.[/yellow]",
                True,
            )
        else:
            list_coverages.append(int(x))

    return list_coverages
