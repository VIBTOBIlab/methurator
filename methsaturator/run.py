from .downsample_utils.methyldackel import run_methyldackel
from .downsample_utils.subsample_bam import subsample_bam
from .config_utils.verbose_utils import vprint
from rich.console import Console
from rich.panel import Panel
import pandas as pd

console = Console()


def downsample(csorted_bams, configs):

    # Create empty dataframes to store results
    reads_df = pd.DataFrame(columns=["Sample", "Percentage", "Read_Count"])
    cpgs_df = pd.DataFrame(columns=["Sample", "Percentage", "Coverage", "CpG_Count"])

    # Loop over bam files, downsampling percentages and minimum coverage values
    for bam in csorted_bams:
        # Start saturation analysis
        console.print(
            Panel(
                f"[bold white]🚀 Running saturation analysis on {bam}[/bold white]",
                border_style="green",
            )
        )
        for pct in configs.percentages:
            for min_cov in configs.coverages:
                vprint(
                    f"[bold]Subsampling BAM file at[/bold] [cyan]{pct}...[/cyan]",
                    configs.verbose,
                )
                results_subsampling_bam, sub_bam = subsample_bam(
                    bam, pct, configs.outdir
                )
                reads_df.loc[len(reads_df)] = results_subsampling_bam
                vprint("[green]✔ Subsampling completed![/green]", configs.verbose)

                vprint(
                    f"[bold]Running MethylDackel:[/bold] minimum coverage [cyan]{min_cov}...[/cyan]",
                    configs.verbose,
                )
                results_subsampling_cov = run_methyldackel(
                    sub_bam, pct, min_cov, configs
                )
                vprint("[green]✔ MethylDackel completed![/green]", configs.verbose)

                cpgs_df.loc[len(cpgs_df)] = results_subsampling_cov

    return cpgs_df, reads_df
