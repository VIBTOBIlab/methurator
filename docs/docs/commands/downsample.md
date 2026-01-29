## `downsample` command

| Option                            | Description                                                                                                        | Default               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- |
| `BAM (positional)`                | Path to a single `.bam` file or multiple files (e.g. `files/*.bam`).                                               | —                     |
| `--outdir, -o`                    | Output directory.                                                                                                  | `./output`            |
| `--fasta`                         | Path to the reference genome FASTA file. If not provided, it will be automatically downloaded based on `--genome`. | —                     |
| `--genome`                        | Genome used for alignment. Options: `hg19`, `hg38`, `GRCh37`, `GRCh38`, `mm10`, `mm39`.                            | —                     |
| `--downsampling-percentages, -ds` | Comma-separated list of downsampling percentages (between 0 and 1, exclusive).                                     | `0.1,0.2,0.4,0.6,0.8` |
| `--minimum-coverage, -mc`         | Minimum CpG coverage to consider for saturation. Can be a single integer or a list (e.g. `1,3,5`).                 | `3`                   |
| `--rrbs`                          | If set, MethylDackel will consider the RRBS nature of the data by adding the `--keepDupes` flag.                   | `False`               |
| `--threads, -@`                   | Number of threads to use during downsampling.                                                                      | All available threads |
| `--keep-temporary-files`          | Keep temporary files after analysis.                                                                               | `False`               |
| `--verbose`                       | Enable verbose logging.                                                                                            | `False`               |
| `--help, -h`                      | Print the help message and exit.                                                                                   | —                     |
| `--version`                       | Print the package version.                                                                                         | —                     |
