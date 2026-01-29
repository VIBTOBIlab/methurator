# 🧬 methurator

**methurator** is a Python package to estimate **CpG sequencing saturation**
for DNA methylation sequencing data. It supports two complementary approaches:

1. Chao's estimator (recommended)
2. Empirical downsampling

---

## Key features

- Extrapolate CpG discovery beyond observed sequencing depth
- Compute theoretical asymptotes
- Optional bootstrap confidence intervals
- Interactive HTML plots
- BioConda and BioContainer support

---

## Installation

=== "Pip"
    !!! note "install dependencies"
        If you install _methurator_ via pip, be sure to install its dependencies [SAMtools](https://www.htslib.org/) and [MethylDackel](https://github.com/dpryan79/MethylDackel).

    ```bash
    pip install methurator
    ```

=== "BioConda"

    ```bash
    conda create -n methurator_env conda::methurator
    conda activate methurator_env
    ```

=== "BioContainer"

    ```bash
    docker pull quay.io/biocontainers/methurator:2.1.0--pyhdfd78af_0
    docker run quay.io/biocontainers/methurator:2.1.0--pyhdfd78af_0 methurator -h
    ```
