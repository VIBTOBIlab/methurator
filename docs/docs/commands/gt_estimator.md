## `gt-estimator` command

| Argument                     | Description                                                                                                        | Default               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- |
| `BAM (positional)`           | Path to a single `.bam` file or multiple files (e.g. `files/*.bam`).                                               | —                     |
| `--outdir, -o`               | Output directory.                                                                                                  | `./output`            |
| `--fasta`                    | Path to the reference genome FASTA file. If not provided, it will be automatically downloaded based on `--genome`. | —                     |
| `--genome`                   | Genome used for alignment. Options: `hg19`, `hg38`, `GRCh37`, `GRCh38`, `mm10`, `mm39`.                            | —                     |
| `--minimum-coverage, -mc`    | Minimum CpG coverage to consider. Can be a single integer or a list (e.g. `1,3,5`).                                | `1`                   |
| `--t-step`                   | Step size for extrapolation factor (`t`) predictions.                                                              | `0.05`                |
| `--t-max`                    | Maximum extrapolation factor (`t`).                                                                                | `10.0`                |
| `--compute_ci`               | Compute confidence intervals using bootstrap replicates.                                                           | `False`               |
| `--bootstrap-replicates, -b` | Number of bootstrap replicates for CI computation.                                                                 | `30`                  |
| `--conf`                     | Confidence level for bootstrap intervals.                                                                          | `0.95`                |
| `--mu`                       | Initial `mu` parameter for the negative binomial distribution in the EM algorithm.                                 | `0.5`                 |
| `--size`                     | Initial `size` parameter for the negative binomial distribution in the EM algorithm.                               | `1.0`                 |
| `--mt`                       | Constraint for rational function approximations.                                                                   | `20`                  |
| `--rrbs`                     | If set to `True`, MethylDackel will use the RRBS flag (`--keepDupes`).                                             | `False`               |
| `--threads, -@`              | Number of threads to use.                                                                                          | Available threads - 2 |
| `--keep-temporary-files, -k` | Keep temporary files after analysis.                                                                               | `False`               |
| `--verbose`                  | Enable verbose logging.                                                                                            | `False`               |
| `--help, -h`                 | Print the help message and exit.                                                                                   | —                     |
| `--version`                  | Print the package version.                                                                                         | —                     |
