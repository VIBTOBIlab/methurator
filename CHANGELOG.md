# CHANGELOG

## [v0.1.9](https://github.com/VIBTOBIlab/methurator/tree/v0.1.9) —

- Add `--no-rrbs` flag to set it on false when running the tool on non RRBS samples.

## [v0.1.8](https://github.com/VIBTOBIlab/methurator/tree/v0.1.8) — 2026-01-03

- Fixed a bug in the plot title naming logic that resulted in all plots having as title the first sample name present in the summary file.
- Fixed some typos in the README.
- Fixed the default number of threads that was not correctly working for HPC environments.

## [v0.1.7](https://github.com/VIBTOBIlab/methurator/tree/v0.1.7) — 2025-12-01

- Made BAM input files positional arguments.
- Slightly updated the sequencing saturation plot.
- Thanks to @ewels for adding a new YAML output file which contains all data in a single file. It also contains run metadata: date, tool version, options etc. for reproducibility and future MultiQC support. An example [here](tests/data/methurator_summary.yml).
- Thanks to @ewels again for some CLI teaks: docstrings for CLI functions, to give intro text; metavars in the help string, to avoid wide column due to --genome options; moved the tool subcommands above --help and --version. Finally, replaced static panel with dynamic Rich progress bar.
- Due to the restructuring above, now `methurator plot` command takes in input the methurator_summary.yml file, to avoid calculating again the sequencing saturation curve.

## [v0.1.6](https://github.com/VIBTOBIlab/methurator/tree/v0.1.6) — 2025-12-01

- Removed `--bamdir` option: if you want to specify more than 1 bam file within a directory you can now simply use the same `--bam` option, specifying all bam files (e.g. --bam files/\*.bam)
- Added Bioconda and Biocontainer instructions on the README.
- Added the --rrbs parameter: if specified (by default), it will add the --keepDups flag to MethylDackel to avoid removal of duplicates.

## [v0.1.5](https://github.com/VIBTOBIlab/methurator/tree/v0.1.5) — 2025-11-23

- Expanded and updated documentation.

## [v0.1.4](https://github.com/VIBTOBIlab/methurator/tree/v0.1.4) — 2025-11-14

- Slightly changed the README and LICENSE files.

## [v0.1.3](https://github.com/VIBTOBIlab/methurator/tree/v0.1.3) — 2025-11-14

### 🎉 Initial Release

**methurator** — a Python package for estimating sequencing saturation in bisulfite sequencing data. Read the [README file](README.md) for more information.
