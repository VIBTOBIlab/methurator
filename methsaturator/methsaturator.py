from .bam_utils import ensure_coordinated_sorted
from .fasta_utils import get_reference
from .methyldackel import run_methyldackel
from .subsample_bam import subsample_bam
from .percentage_utils import percentage_checker
from .coverage_utils import mincoverage_checker
from .plot_utils.plot_curve import plot_curve
from .verbose_utils import vprint
from .bam_dir_utils import import_bam_files
from .cleanup_utils import clean_up
import rich_click as click
from rich.console import Console
from rich.panel import Panel
import os
import pandas as pd


console = Console()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--bam",
    type=click.Path(exists=True),
    required=False,
    help="BAM input file to compute methylation saturation.",
)
@click.option(
    "--bamdir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=False,
    help="Directory containing multiple BAM files.",
)
@click.option(
    "--outdir",
    type=click.Path(),
    default="seqsaturation_output",
    help="Default output directory.",
)
@click.option(
    "--fasta",
    type=click.Path(exists=True),
    help="Fasta file of the reference genome used to align the samples. "
    "If not provided, it will download it according to the specified genome.",
)
@click.option(
    "--genome",
    type=click.Choice(["hg19", "hg38", "GRCh37", "GRCh38", "mm10", "mm39"]),
    default=None,
    help="Genome used to align the samples.",
)
@click.option(
    "--downsampling-percentages",
    "-ds",
    default="0.1,0.25,0.5,0.75",
    help="Percentages used to downsample the .bam file. Default: 0.1,0.25,0.5,0.75",
)
@click.option(
    "--minimum-coverage",
    "-mc",
    default="3",
    help="Minimum CpG coverage to estimate sequencing saturation. It can be either a single integer or a list of integers (e.g 1,3,5). Default: 3",
)
@click.option(
    "--keep-temporary-files",
    "-k",
    is_flag=True,
    help="If set to True, temporary files will be kept after the analysis. Default: False",
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def run_cli(
    bam,
    bamdir,
    outdir,
    fasta,
    genome,
    downsampling_percentages,
    minimum_coverage,
    keep_temporary_files,
    verbose,
):
    """Package for sequencing saturation analysis of sequencing methylation data."""

    # Enforce that at least one of --fasta or --genome is provided
    if fasta is None and genome is None:
        raise click.UsageError(
            "Error: you must provide in input either --fasta or --genome"
        )

    # Enforce that at least one of --bam or --bamdir is provided
    if bam is None and bamdir is None:
        raise click.UsageError(
            "Error: you must provide in input either --bam or --bamdir"
        )

    # Print I/O parameters
    params_text = ""
    params_text += f"[purple]Output directory:[/purple] [blue]{outdir}[/blue]\n"
    if fasta is not None:
        params_text += f"[purple]Reference FASTA:[/purple] [blue]{fasta}[/blue]\n"
    if genome is not None:
        params_text += f"[purple]Genome:[/purple] [blue]{genome}[/blue]\n"
    params_text += f"[purple]Downsampling percentages:[/purple] [blue]{downsampling_percentages}[/blue]\n"
    params_text += (
        f"[purple]Minimum coverage values:[/purple] [blue]{minimum_coverage}[/blue]\n"
    )
    params_text += (
        f"[purple]Keep temporary files:[/purple] [blue]{keep_temporary_files}[/blue]"
    )
    console.print(
        Panel(
            params_text,
            title="📌 [bold cyan]Input / Output Parameters[/bold cyan]",
            border_style="cyan",
            expand=False,
        )
    )

    # Create output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
        vprint(f"[bold]Created output directory {outdir}...[/bold]", verbose)

    # Run checks on fasta file if provided or download it
    try:
        fasta = get_reference(genome, fasta, outdir, verbose)
    except ValueError as e:
        raise click.UsageError(f"{e}")

    # If bamdir is provided, import all bam files in the directory
    if bamdir and bam:
        vprint(
            "[yellow]⚠️ Warning: both --bam and --bamdir were provided. Only --bamdir will be considered.[/yellow]",
            True,
        )
    csorted_bams = []
    if bamdir:
        raw_bam_files = import_bam_files(bamdir)
        vprint(
            f"[bold]Found {len(raw_bam_files)} BAM files in directory '{bamdir}'.[/bold]",
            verbose,
        )
        for bam in raw_bam_files:
            # Check if bam file coordinate-sorted or sort it
            try:
                csorted_bam = ensure_coordinated_sorted(bam, verbose)
                csorted_bams.append(csorted_bam)
            except ValueError as e:
                raise click.UsageError(f"{e}")
    else:
        try:
            csorted_bam = ensure_coordinated_sorted(bam, verbose)
            csorted_bams.append(csorted_bam)
        except ValueError as e:
            raise click.UsageError(f"{e}")

    # Check that downsampling percentages and minimum coverage values are valid
    try:
        percentages = percentage_checker(downsampling_percentages)
    except ValueError as e:
        raise click.UsageError(f"{e}")
    try:
        coverages = mincoverage_checker(minimum_coverage)
    except ValueError as e:
        raise click.UsageError(f"{e}")

    # Create empty dataframes to store results
    reads_df = pd.DataFrame(columns=["Sample", "Percentage", "Read_Count"])
    cpgs_df = pd.DataFrame(columns=["Sample", "Percentage", "Coverage", "CpG_Count"])
    # file_name = os.path.basename(bam).split(".", 1)[0]

    # Loop over bam files, downsampling percentages and minimum coverage values
    for csorted_bam in csorted_bams:
        # Start saturation analysis
        console.print(
            Panel(
                f"[bold white]🚀 Running saturation analysis on {csorted_bam}[/bold white]",
                border_style="green",
            )
        )
        for pct in percentages:
            for min_cov in coverages:
                vprint(
                    f"[bold]Subsampling BAM file at[/bold] [cyan]{pct}...[/cyan]",
                    verbose,
                )
                results_subsampling_bam, sub_bam = subsample_bam(bam, pct, outdir)
                reads_df.loc[len(reads_df)] = results_subsampling_bam
                vprint("[green]✔ Subsampling completed![/green]", verbose)

                vprint(
                    f"[bold]Running MethylDackel:[/bold] minimum coverage [cyan]{min_cov}...[/cyan]",
                    verbose,
                )
                results_subsampling_cov = run_methyldackel(
                    sub_bam, pct, fasta, outdir, min_cov
                )
                vprint("[green]✔ MethylDackel completed![/green]", verbose)

                cpgs_df.loc[len(cpgs_df)] = results_subsampling_cov

    # Save the dataframes as CSV files and plot the saturation curve
    reads_df.to_csv(os.path.join(outdir, "reads_summary.csv"), index=False)
    cpgs_df.to_csv(os.path.join(outdir, "cpgs_summary.csv"), index=False)
    plot_curve(cpgs_df, reads_df, percentages, outdir)
    if not keep_temporary_files:
        clean_up(outdir)


if __name__ == "__main__":
    run_cli()
