import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from .math_model import asymptotic_growth

# ===============================================================
# Plotting Functions
# ===============================================================


def plot_error_data(x_data, y_data, reads, output_path, title, error):
    """Plot the data when curve fitting fails."""
    x_pred = np.append(x_data, [1.2, 1.4, 1.6, 1.8, 2.0])
    x_pred_reads = reads * x_pred

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(x_data, y_data, "o", color="blue")

    ax1.set_xticks(x_pred)
    ax1.set_title(f"{title}\n{error}", fontsize=12, color="red", loc="left")
    ax1.set_xlabel("Percentage of downsampling", fontsize=14)
    ax1.set_ylabel("Number of CpGs", fontsize=14)
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Add secondary x-axis for read counts
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(x_pred)
    ax2.tick_params(axis="x", pad=7)
    ax2.set_xticklabels([f"{x:.1e}" for x in x_pred_reads], rotation=45)
    ax2.set_xlabel("Number of reads", fontsize=14)

    fig.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"⚠️  Curve fitting failed. Plot saved to {output_path}")


def plot_data(x_data, y_data, reads, asymptote, params, output_path, title):
    """Plot data and fitted curve for a single sample."""
    x_pred = np.append(x_data, [1.2, 1.4, 1.6, 1.8, 2.0])
    x_pred_reads = reads * x_pred
    y_pred = asymptotic_growth(x_pred, *params)
    y_diff = [0, 1] + [(y_pred[i] / asymptote) * 100 for i in range(2, len(y_pred))]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Raw data + fit
    ax1.plot(x_data, y_data, "o", color="blue")
    ax1.plot(x_pred, y_pred, "g-", label=f"fit: β₀={params[0]:.3f}, β₁={params[1]:.3f}")
    ax1.plot(x_pred, y_pred, "|", color="black", markersize=10)

    # Add percentage annotations
    for i in range(3, len(x_pred)):
        ax1.text(
            x_pred[i],
            y_pred[i] - 0.09 * y_pred[i],
            f"{y_diff[i]:.1f}%",
            color="black",
            fontsize=10,
            ha="center",
        )

    # Add asymptote line
    ax1.axhline(y=asymptote, color="grey", linestyle="--")
    ax1.text(
        0,
        asymptote - asymptote * 0.05,
        f"Asymptote = {asymptote:.2e}",
        color="grey",
        fontsize=12,
    )

    # Formatting
    ax1.set_title(title, fontsize=16, loc="left")
    ax1.set_xlabel("Percentage of downsampling", fontsize=14)
    ax1.set_ylabel("Number of CpGs", fontsize=14)
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Secondary axis for reads
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(x_pred)
    ax2.tick_params(axis="x", pad=7)
    ax2.set_xticklabels([f"{x:.1e}" for x in x_pred_reads], rotation=45)
    ax2.set_xlabel("Number of reads", fontsize=14)

    # Legend
    leg_patch = mpatches.Patch(
        label=r"% : Sequencing saturation ($\frac{\hat{y}}{\text{asymptote}} \times 100$)"
    )
    plt.legend(
        handles=[leg_patch], loc="lower right", handletextpad=-1.0, handlelength=0
    )

    fig.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Plot saved to {output_path}")
