---
title: "Methurator: a python package for CpG-level sequencing saturation analysis of methylation data."
tags:
  - Python
  - Biology
  - DNA methylation
  - CpGs
  - Sequencing saturation
authors:
  - name: Edoardo Giuili
    orcid: 0000-0003-2763-3767
    affiliation: "1, 2"
  - name: Philip Ewels
    orcid: 0000-0003-4101-2502
    affiliation: 3
  - name: Sam Kint
    orcid: 0000-0002-6719-2903
    affiliation: "1, 2"
  - name: Katleen De Preter
    orcid: 0000-0002-7726-5096
    affiliation: "1, 2"
affiliations:
  - name: VIB Center for Medical Biotechnology & VIB.AI, VIB, Technologiepark 75 9052 Zwijnaarde, Belgium
    index: 1
  - name: Cancer Research Institute Ghent (CRIG), 9000 Ghent, Belgium
    index: 2
  - name: Seqera, Carrer de Marià Aguiló, 28, Barcelona, 08005, Spain
    index: 3
date: 23 March 2026
bibliography: paper.bib
---

# Summary

**Methurator** is a Python package designed to estimate CpG-level
sequencing saturation in DNA methylation sequencing data. To do so,
methurator first uses BAM files to extract CpG coverage information
using MethylDackel. Next, it fits the Chao estimator, as described in
preseqR, taking the observed CpG counts as input. Finally, it
extrapolates the data and estimates CpG coverage at hypothetical higher
sequencing depths and measures the saturation relative to the estimated
maximum CpGs covered in the sequencing library. Methurator can compute
CpG saturation for most of DNA methylation sequencing data, such as
whole-genome bisulfite sequencing (WGBS), reduced-representation
bisulfite sequencing (RRBS) and EM-seq data.

# Statement of Need

Sequencing saturation (ρ) is typically used to estimate the fraction of
the library complexity that was sequenced [@daley_predicting_2013]. It is expressed
as a percentage and indicates the extent to which additional sequencing
depth (increased total number of reads) yields gradually decreasing
returns, in terms of newly detected features. These features may include
genes, unique molecular identifiers (UMIs), or newly observed CpG sites
in DNA methylation experiments.

In general, sequencing saturation can be calculated as:

$$\rho_{N} = 1 - \frac{M}{N}$$

where N corresponds to the number of sequenced reads, and M corresponds
to the number of features detected.

In libraries for DNA methylation sequencing use of UMIs is uncommon, and
saturation is typically estimated using unique reads after
deduplication. For this, deduplication tools such as
_deduplicate_bismark_ [@krueger_bismark_2011] or _Picard
MarkDuplicates_ [@noauthor_picard_nodate] identify PCR duplicates by comparing genomic
alignment coordinates: chromosome name and 5' start position (and 3' end
for paired-end experiments). Reads with identical coordinates are
assumed to originate from the same DNA fragment and are marked as
duplicates. Sequencing saturation is then calculated as the fraction of
unique (deduplicated) to total reads. Tools like Preseq [@daley_predicting_2013]
allow extrapolation of library complexity to predict saturation at
higher sequencing depths.

However, for DNA methylation sequencing, estimating read-level
saturation alone is often insufficient. In many applications, it is more
meaningful to quantify the number of CpG sites covered by a minimum read
depth: differential methylation analyses typically require coverage of
at least 5x–15x per CpG [@ziller_coverage_2015]. Although unique read–based
saturation indicates overall library complexity, it does not inform how
many additional reads are required to achieve sufficient CpG coverage.
This factor is influenced by reference genome length, type of experiment
(single- or paired-end) and read length. Moreover, duplicate-based
approaches are not reliable for restriction enzyme-based methods such as
reduced representation bisulfite sequencing (RRBS) [@meissner_reduced_2005]. In RRBS
the CpG density is enriched by employing the restriction enzyme MspI,
which cuts at C^CGG sites and generates fragments with fixed genomic
boundaries. Consequently, many independent DNA fragments share identical
start and end coordinates and would incorrectly be classified as PCR
duplicates, preventing accurate saturation estimation using conventional
methods.

Preseq was originally implemented to estimate library complexity using
BAM files with the function _lc_extrap_, by identifying unique and
duplicated reads. Later, **_gc_extrap_** was introduced to predict
genomic coverage, using the number of new bases covered at least once at
increasing sequencing depth [@daley_modeling_2014]. Subsequent methodological
advances generalized this framework to estimate the number of features
observed at least _r_ times (e.g. the number of features observed at
least 3 times) if a new sample would be taken [@deng_estimating_2018]. This
generalized estimator, referred to as Chao estimator, was implemented in
the **preseqR** package and applied to estimate species richness.
However, unlike the original Preseq implementation, preseqR was not
designed to operate directly on BAM files within standard bioinformatics
pipelines. Instead, it requires a precomputed frequency-of-frequencies
matrix as input, such as the number of CpGs observed with coverage
counts.

Methurator addresses this limitation by integrating the Chao estimator
method into a Python package that operates directly on BAM files. The
workflow 1) extracts methylation coverage using MethylDackel; 2)
computes the frequency-of-frequencies matrix for CpG coverage; 3) fits
the Chao estimator with this matrix; 4) estimates the number of CpG
sites covered at increasing sequencing depth. The package also provides
interactive HTML visualizations of the results. Importantly, because
methurator relies on coverage distributions rather than read duplicates
identification, it enables reliable saturation analysis for RRBS data as
well, making it the first tool that can do this.

# Overview

## Installation

Methurator is a wrapper around SAMtools [@li_sequence_2009] and
MethylDackel [@ryan_dpryan79methyldackel_2025] and therefore requires these two tools to be
installed. Methurator itself can then be installed via PyPi as follows:

**~ $ pip install methurator**

Alternatively, it is available through Bioconda [@gruning_bioconda_2018] and
Biocontainers [@da_veiga_leprevost_biocontainers_2017], in which cases SAMtools and MethylDackel are
automatically installed.

## Methodology

Methurator implements the Chao estimator from preseqR [@deng_estimating_2018]. The
package takes one or multiple BAM files and the FASTA file of the genome
used to align the samples as input. Then, it extracts the CpG
methylation using MethylDackel and creates a matrix where the first
column represents the CpG coverage frequency (e.g., 1, 2, 3, … reads
covering a CpG), while the second column indicates the number of CpG
sites observed at each coverage level. This matrix is then used to fit
the Chao estimator, which is subsequently used for extrapolation to
predict the number of CpG sites that would be covered at least _r_ times
at higher sequencing depth _t_. The extrapolation factor _t_ represents
the ratio of hypothetical reads to observed reads:

$$t = \frac{hypothetical\ reads}{observed\ reads}$$

When _t = 1_, the hypothetical reads correspond to the currently
observed reads. When _t = 2_, we estimate the number of CpGs covered at
least _r_ times at a sequencing depth that is twice the observed depth.

In addition, the package estimates CpG sequencing saturation by dividing
the predicted number of CpGs at each _t_ by a proxy of the asymptote of
the curve. This proxy corresponds to the predicted number of CpG sites
at _t = 1000_ (i.e., a sequencing depth 1000 times higher than the
observed dataset). Although such depth is usually not realistic in
practice, it serves as a practical approximation of a fully saturated
experiment (~100% CpG coverage). Finally, methurator can also quantify
confidence intervals through bootstrap resampling, if enabled.

## Example workflow

### gt-estimator command

The _gt-estimator_ command requires one or more BAM files as input and
the FASTA file or genome name of the reference genome used to align the
samples. If the user specifies only the genome (e.g., hg19), methurator
will automatically download the corresponding FASTA file. Example:

**~ $ methurator gt-estimator SRR3652697.bam SRR3652697sub10.bam
--genome hg19 --minimum-coverage 1**

In this example, we run the command using a --_minimum-coverage_
parameter of 1, corresponding to an estimator _r = 1_. This command
outputs a summary YAML file (methurator*summary.yml) which contains the
interpolated and extrapolated data points that will be used by the
\_plot* command to visualize the results. It also contains run metadata
to enhance reproducibility of the analyses.

### plot command

The _plot_ command plots the curve described above. This command needs
the YAML summary file created by the previous command as input:

**~ $ methurator plot --summary methurator_summary.yml**

This command will generate an interactive HTML plot for each sample
analyzed, describing the sequencing saturation curve. A flattening curve
indicates that saturation is being reached.

![Example of plots generated by methurator plot command. **(A)** SRR3652697 sample that reached saturation with a minimum coverage r = 1; **(B)** SRR3652697 downsampled at 10% that reached only 47.6% of saturation, indicating that additional sequencing depth would be beneficial. The asymptote is displayed as a dashed grey line.](Figure_1.png)

Within the interactive plot, users can examine sequencing saturation,
number of CpGs and number of reads at each sequencing depth _t_
(Supplementary Figure 1).

## Estimator’s performance

To provide a comprehensive evaluation of the package, we assessed Chao
estimator on three datasets: (i) three RRBS samples, (ii) three
deduplicated WGBS samples, and (iii) three non-deduplicated WGBS
samples. All samples were downloaded from NCBI and processed using the
nf-core/methylseq pipeline (version 4.2.0) [@ewels_nf-core_2020; @ewels_nf-coremethylseq_2025]. For more
detailed information on the sample IDs and pipeline parameters, consult
the Documentation and Availability section.

The resulting BAM files were downsampled to 10%, 50%, and 80% of their
original read counts. For each downsampled file, we then predicted the
number of CpGs that would be observed at full sequencing depth (100%)
using four coverage thresholds (r = 1, 5, 10, and 15). To evaluate
prediction performance, we compared the predicted and observed numbers
of CpGs for each coverage threshold r. The observed CpGs were defined as
the number of CpG sites detected in the original sample at full
sequencing depth (100%). Estimation accuracy was quantified using the
percentage error:

$$\text{Percentage error}_{r} = \frac{\mid N_{\text{r, observed}} - N_{\text{r, predicted}} \mid}{N_{\text{r, observed}}} \times 100$$

where _N_ represents the number of CpGs at a given _r_.

As shown in Table 1, and consistent with results previously reported by
the authors of the estimator for a similar application [@deng_estimating_2018], the
estimator achieved percentage errors below 3% across most conditions.
The only exception was observed for non-deduplicated WGBS samples at
*r* = 15. Notably, for both RRBS and non-deduplicated WGBS datasets, the
standard deviation frequently exceeded the mean error, indicating
increased variability and suggesting that duplicate reads negatively
affect estimator performance. These findings highlight the importance of
using deduplicated BAM files for accurate CpG saturation estimation,
whenever deduplication is feasible, such as in WGBS experiments or when
using UMIs.

| Type                   | r = 1 mean/std (%) | r = 5 mean/std (%) | r = 10 mean/std (%) | r = 15 mean/std (%) |
| :--------------------- | :----------------- | :----------------- | :------------------ | :------------------ |
| RRBS                   | 2.71 / 5.48        | 0.83 / 1.81        | 1.01 / 2.18         | 0.70 / 1.34         |
| WGBS (deduplicated)    | 0.74 / 0.44        | 0.66 / 0.38        | 0.70 / 0.89         | 2.40 / 1.97         |
| WGBS (with duplicates) | 0.77 / 0.79        | 1.78 / 1.66        | 1.72 / 2.00         | 8.66 / 12.58        |

: Matrix representing percentage errors of Chao estimator on RRBS, deduplicated and non-deduplicated WGBS samples at each minimum coverage threshold r. The mean and standard deviation (std) were calculated across the three downsampling fractions used (10%, 50%, 80%).

# Documentation and Availability

Methurator is available in PyPi
(<https://pypi.org/project/methurator/>), BioConda
(<https://anaconda.org/channels/bioconda/packages/methurator/overview>)
and BioContainers
(<https://quay.io/repository/biocontainers/methurator>). Methurator is
also supported by MultiQC [@ewels_multiqc_2016] (&gt;=v1.34). Methurator source
code is available on GitHub (<https://github.com/VIBTOBIlab/methurator>)
under the open-source MIT license, with extensive documentation and a
more detailed description of all configurable parameters at
[https://vibtobilab.github.io/methurator/](https://vibtobilab.github.io/methurator/latest/).
Details on the sample preprocessing steps used to evaluate the
estimator’s performance and to reproduce the analyses are available at:
<https://github.com/VIBTOBIlab/methurator_paper>.

# Acknowledments

We acknowledge the use and support of the VIB Data Core facility. We
also thank the HPC-UGent team for their support. This project was
supported by Kom op tegen Kanker \[11559\], the European Research
Council (ERC) under the European Union’s (Horizon2020 research and
innovation programme) \[101044243\] and the Fonds Wetenschappelijk
Onderzoek (FWO) PhD Fellowship \[1126825N\].

# References
