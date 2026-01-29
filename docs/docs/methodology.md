## How do we compute the sequencing saturation?

### 1. Chao Estimator approach (best practise)

**methurator gt-estimator** uses an approach developed in 2018 by [Chao Deng et al](https://arxiv.org/abs/1607.02804) and further implemented in [preseqR](https://github.com/smithlabcode/preseqR). This approach builds on the theoretical nonparametric empirical Bayes foundation of **Good and Toulmin (1956)**, to model sequencing saturation and extrapolate to higher sequencing depths. The model implemented in **preseqR** was mirrored here and tailored toward sequencing saturation application. The workflow consists of the following steps:

1. **Extracts CpGs** from BAM files using MethylDackel
2. **Fits the model implemented by Chao Deng et al** taking in input the observed CpG counts
3. **Predicts future CpG discovery** using rational function approximations
4. **Quantifies confidence intervals** through bootstrap resampling (if enabled)

The extrapolation factor (t) represents the ratio of hypothetical total reads to actual observed reads. Values of t ≤ 1 correspond to **interpolation** (between observed data points), while t > 1 represents **extrapolation** (prediction beyond observed depth).

For a given coverage level:

- At t = 1: prediction matches observed CpGs, and the number of reads at full sequencing depth is reported in the summary file
- As t increases: predictions approach the theoretical asymptote (maximum CpGs at t = 1000, shown in the plot and used for saturation calculation)

### 2. Downsample approach

To calculate the **sequencing saturation** of an DNAm sample when using the `downsample` command, we adopt the following strategy. For each sample, we downsample it according to 4 different percentages (default: `0.1,0.2,0.4,0.6,0.8`). Then, we compute the number of **unique CpGs covered by at least 3 reads** and the **number of reads** at each downsampling percentage.

We then fit the following curve using the `scipy.optimize.curve_fit` function:

$$
y = \beta_0 \cdot \arctan(\beta_1 \cdot x)
$$

We chose the **arctangent function** because it exhibits an **asymptotic growth** similar to sequencing saturation.
For large values of $\text{x}$ (as $\text{x} \to \infty$), the asymptote corresponds to the theoretical maximum number of **unique CpGs covered by at least 3 reads** and can be computed as:

$$
\text{asymptote} = \beta_0 \cdot \frac{\pi}{2}
$$

Finally, the **sequencing saturation value** can be calculated as following:

$$
\text{Saturation} = \frac{\text{Number of unique CpGs (≥3 counts)}}{\text{Asymptote}}
$$

This approach allows estimation of the theoretical **maximum number of CpGs** that can be detected given an infinite sequencing depth, and quantifies how close the sample is to reaching sequencing saturation.
