# Quick Start

## Option A: Chao Estimator (best practise)

The `gt-estimator` command estimates CpGs sequencing saturation at higher depth than the observed one. This is the recommended approach for extrapolation analysis.

```bash
methurator gt-estimator --fasta tests/data/genome.fa tests/data/Ecoli.csorted.bam
```

This command generates:

- **Summary YAML file** (`methurator_summary.yml`) — Contains metadata, model parameters, and extrapolation results with:
  - Extrapolation factor (t) values from 0 to `--t-max` (default: 10.0)
  - Boolean indicating interpolated (t ≤ 1) vs extrapolated (t > 1) data
  - Total CpGs predicted at each t value
  - Theoretical asymptote (maximum CpGs, computed at t = 1000)
  - Number of reads observed at full sequencing depth (t = 1)
  - Confidence intervals (if `--compute_ci` is enabled)

## Option B: Downsample

The `downsample` command performs BAM downsampling according to specified percentages and coverage levels:

```bash
methurator downsample --fasta tests/data/genome.fa tests/data/Ecoli.csorted.bam
```

This command generates:

- **CpG summary** (`methurator_cpgs_summary.yml`)— number of unique CpGs detected in each downsampled BAM
- **Reads summary** (`methurator_reads_summary.yml`) — number of reads in each downsampled BAM
- **Summary YAML** (`methurator_summary.yml`) — consolidated file with all data and run metadata

## Plot the sequencing saturation curve

Use the `plot` command to visualize the results, including the asymptote line and the number of reads at each t:

```bash
methurator plot --summary output/methurator_summary.yml
```
