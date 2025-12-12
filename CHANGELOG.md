# CHANGELOG

## [v0.1.7](https://github.com/VIBTOBIlab/methurator/tree/v0.1.7) — 2025-12-01

- Made bam input files positional arguments.
- Slightly changed the sequencing saturation plot.

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
