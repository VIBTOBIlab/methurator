## Methsaturator package

Welcome to methsaturator package. This Python package is intended to be used mainly for reduced-represantion bisulfite sequencing (RRBS) data, since for whole genome bisulfite sequencing data, or other whole genome methylation data (e.g. EMseq) the [Preseq](https://smithlabresearch.org/software/preseq/) package can be used. However, methsaturator should work just fine on this data as well.

### Installation

### How to run it

To run the package, you need to provide in input the bam (`--bam`) file for which you want to calculate the sequencing saturation or a directory containing multiple bam files (`--bamdir`). Moreover, you need to specify either the reference genome used to align the sample (run `methsaturator -h` to check the available genomes), in which case the tool will automatically download and save it in the output directory, or directly the fasta file.

```python
methsaturator --genome hg19 --bam test_data/SRX1631721.markdup.sorted.csorted.bam
```

### Usage

`--bam`

Path to the .bam file to compute sequencing saturation.

`--bamdir`

Directory containing multiple BAM files.

`--outdir`

Output directory. Default is **./seqsaturation_output**.

`--fasta`

Fasta file of the reference genome used to align the samples. If not provided, it will be downloaded according to the genome specifed in the **--genome** parameter.

`--genome`

Genome used to align the samples. Available: **[hg19|hg38|GRCh37|GRCh38|mm10|mm39]**

`--downsampling-percentages`

By default, the package will subsample the bam file using [SAMtools](https://www.htslib.org/) according to the following pecentages: `0.1,0.25,0.5,0.75`. However, the user can use their own percentages with the **--downsampling-percentages** (-ds) parameter. It has to be a string of comma separated decimals between 0 and 1 (exclusive).

`--minimum-coverage`

Minimum CpG coverage to estimate sequencing saturation. It can be either a single integer or a list of integers (e.g 1,3,5). Default: 3.

`--keep-temporary-files`

If set to True, temporary files will be kept after the analysis. Default: False.
