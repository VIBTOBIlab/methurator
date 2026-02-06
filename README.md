# 🧬 methurator

[![Python](https://img.shields.io/badge/python-≥3.10%20&%20≤3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-blue.svg)](https://pytest.org/)
[![BioConda](https://img.shields.io/badge/bioconda-methurator-brightgreen.svg?logo=anaconda)](https://anaconda.org/bioconda/methurator)
[![BioContainer](https://img.shields.io/badge/biocontainer-methurator-0A7BBB.svg?logo=docker)](https://quay.io/repository/biocontainers/methurator)

---

## 🚀 What is methurator?

> **Note**: For detailed documentation, command reference, and advanced usage, see the [docs here](https://vibtobilab.github.io/methurator/latest/).

**methurator** is a Python package to estimate CpG sequencing saturation for DNA methylation sequencing data.

---

## ✨ Key features

- Extrapolate CpG discovery beyond observed sequencing depth
- Compute theoretical asymptotes
- Optional bootstrap confidence intervals
- Interactive HTML plots
- BioConda and BioContainer support

## 📦 Installation

### pip

```bash
pip install methurator
```

### BioConda (recommended)

```bash
conda create -n methurator_env methurator
conda activate methurator_env
```

### Container

```bash
docker pull quay.io/biocontainers/methurator
```

## Example Workflow

```bash
# Run Chao estimator on BAM file
methurator gt-estimator --genome hg19 my_sample.bam --compute_ci

# Generate plots from the results
methurator plot --summary output/methurator_summary.yml
```
