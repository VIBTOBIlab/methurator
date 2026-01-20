import rich_click as click
from rich.console import Console
from rich.panel import Panel
import importlib.metadata
from methurator.gt_utils.run_estimator import run_estimator
from methurator.gt_utils.config_validator import GTConfig

console = Console()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument(
    "covs",
    type=click.Path(),
    required=True,
    nargs=-1,
    help="Path to a single .cov file or to multiple ones (e.g. files/*.cov).",
)
@click.option(
    "--minimum-coverage",
    "-mc",
    type=int,
    default=1,
    help="Minimum CpG coverage to estimate sequencing saturation. "
    "It can be either a single integer or a list of integers (e.g 1,3,5). Default: 3",
)
@click.option(
    "--t-step",
    default=0.05,
    help="Step size taken when predicting future unique CpGs at increasing depth. Default: 0.05",
)
@click.option(
    "--k-max",
    default=27,
    help="Maximum number of frequencies to consider when predicting future unique CpGs at increasing depth. Default: 27",
)
@click.option(
    "--bootstrap-replicates",
    "-b",
    default=100,
    help="Number of bootstrap replicates. Default: 100",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(),
    default="output",
    help="Default output directory.",
)
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
@click.version_option(importlib.metadata.version("methurator"))
def gt_estimator(covs, **kwargs):
    """Fit the Good-Toulmin estimator."""

    # Import and validate params
    configs = GTConfig(covs, **kwargs)

    # Print I/O parameters
    params_text = ""
    params_text += f"[bold]Input coverage files:[/bold] {', '.join(configs.covs)}\n"
    params_text += f"[bold]Output directory:[/bold] {configs.outdir}\n"
    params_text += f"[bold]Minimum coverage:[/bold] {configs.minimum_coverage}\n"
    params_text += f"[bold]t step size:[/bold] {configs.t_step}\n"
    params_text += f"[bold]k max:[/bold] {configs.kmax}\n"
    params_text += (
        f"[bold]Number of bootstrap replicates:[/bold] {configs.bootstrap_replicates}\n"
    )
    params_text += f"[bold]Verbose:[/bold] {configs.verbose}"
    console.print(
        Panel(
            params_text,
            title="📌 [bold cyan]Input / Output Parameters[/bold cyan]",
            border_style="cyan",
            expand=False,
        )
    )

    # Fit the model
    run_estimator(configs)
