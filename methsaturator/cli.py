import rich_click as click
from .plot import plot
from .downsample import downsample


@click.group()
def entry_point():
    pass


# Register the 2 subcommands: downsample and plot
entry_point.add_command(plot)
entry_point.add_command(downsample)

if __name__ == "__main__":
    entry_point()
