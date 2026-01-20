import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


def build_frequency_of_frequencies(cov, min_cov):
    """
    Build frequency-of-frequencies from coverage DataFrame.

    Args:
        df: pandas DataFrame with 'coverage' column.
    Returns:
        f: dict mapping coverage k to number of CpGs with that coverage (f_k).
    """
    df = pd.read_csv(
        cov,
        sep="\t",
        header=None,
        skiprows=1,
        low_memory=False,
        names=["chr", "start", "end", "methylation", "mcounts", "unmcounts"],
    )
    df["coverage"] = df["mcounts"] + df["unmcounts"]
    df = df[df["coverage"] >= min_cov]
    total_cpgs = df.shape[0]

    # Only use CpGs with coverage >= 1
    coverages = df["coverage"].values

    # Count frequency-of-frequencies
    freq_of_freq = Counter(coverages)  # f_k = number of CpGs with coverage k

    # Optional: convert to dict for GT function
    f = dict(freq_of_freq)

    return f, total_cpgs


def good_toulmin(f, t, k_max):
    """
    Euler-transformed Good-Toulmin estimator for new CpGs.

    ΔC(t) = sum_{j>=1} (-1)^{j+1} (t-1)^j n_j
    """
    js = np.array(sorted(f.keys()))
    njs = np.array([f[j] for j in js])

    if k_max is not None:
        mask = js <= k_max
        js = js[mask]
        njs = njs[mask]

    deltaC = np.sum((-1) ** (js + 1) * njs * ((t - 1) ** js))
    return deltaC


def bootstrap_gt(f, t, estimator_fn, n_boot, kmax, random_state):
    """
    Parametric bootstrap for Good-Toulmin-type estimators.

    Args:
        f: dict {k: n_k}
        t: extrapolation factor
        estimator_fn: function(f, t) -> estimate
        n_boot: number of bootstrap replicates
        k_max: optional truncation
        random_state: seed

    Returns:
        point_estimate, (ci_low, ci_high), bootstrap_samples
    """
    rng = np.random.default_rng(random_state)

    # point estimate
    point = estimator_fn(f, t, kmax)

    boot_estimates = []
    ks = np.array(sorted(f.keys()))
    nks = np.array([f[k] for k in ks])

    for _ in range(n_boot):
        # Poisson bootstrap of histogram
        nks_star = rng.poisson(nks)

        f_star = {k: nks_star[i] for i, k in enumerate(ks) if nks_star[i] > 0}
        try:
            est = estimator_fn(f_star, t, kmax)
            boot_estimates.append(est)
        except Exception:
            continue

    boot_estimates = np.array(boot_estimates)
    ci_low, ci_high = np.percentile(boot_estimates, [2.5, 97.5])

    return (
        round(float(point), 2),
        (round(float(ci_low), 2), round(float(ci_high), 2)),
        boot_estimates,
    )


def plot_gt_curve(df):

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))

    plt.plot(df["t"], df["total_cpgs"])

    plt.fill_between(df["t"], df["ci_low"], df["ci_high"], alpha=0.3)
    plt.xlabel("t (Extrapolation Factor)")
    plt.ylabel("Predicted Unique CpGs")
    plt.title("Good-Toulmin Estimator Saturation Curve")
    plt.legend()
    plt.tight_layout()
    plt.show()


def run_estimator(configs):

    df = pd.DataFrame(
        columns=["sample", "t", "method", "ci_low", "ci_high", "total_cpgs"]
    )
    # Run estimator for each coverage file
    for cov in configs.covs:

        # Compute frequency-of-frequencies and total CpGs for the given minimum coverage
        f, total_cpgs = build_frequency_of_frequencies(cov, configs.minimum_coverage)

        # Calculate estimates for each t in [0, 2] with step t_step
        for t in np.arange(0, 2 + configs.t_step, configs.t_step):

            t = round(float(t), 2)
            res_list = []

            gt_point, gt_ci, _ = bootstrap_gt(
                f, t, good_toulmin, configs.bootstrap_replicates, configs.kmax, 42
            )
            res_list += [
                cov,
                t,
                "raw_gt",
                total_cpgs + gt_ci[0],
                total_cpgs + gt_ci[1],
                total_cpgs + gt_point,
            ]

            df = pd.concat(
                [df, pd.DataFrame([res_list], columns=df.columns)], ignore_index=True
            )
    plot_gt_curve(df)
    print(df)
