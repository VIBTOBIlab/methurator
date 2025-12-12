import numpy as np
from rich.console import Console
from methurator.plot_utils.math_model import asymptotic_growth
import plotly.graph_objs as go

# ===============================================================
# Plotting Functions
# ===============================================================

console = Console()


def human_readable(num):
    """Format large numbers into human-readable form (e.g., 1.5K, 2.3M, 1.1B)."""
    for unit, divisor in [("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if num >= divisor:
            return f"{num/divisor:.1f}{unit}"
    return str(int(num))


def fmt_list(values):
    """Round and convert a list of numbers to human-readable strings."""
    return [human_readable(round(v, 0)) for v in values]


def make_base_plot(title, xaxis="Number of reads", yaxis="Number of CpGs"):
    """Create a preformatted Plotly figure."""
    fig = go.Figure()
    fig.update_xaxes(title_text=xaxis, showgrid=True)
    fig.update_yaxes(title_text=yaxis, showgrid=True)
    fig.update_layout(
        title=dict(text=title, x=0.5, y=0.9),
        width=950,
        height=620,
        template="plotly_white",
        showlegend=False,
    )
    return fig


def plot_fallback(plot_obj):
    """Fallback plot when curve fitting fails."""
    x_reads = fmt_list([x * plot_obj.reads for x in plot_obj.x_data])
    y_cpgs = fmt_list(plot_obj.y_data)

    fig = make_base_plot(f"{plot_obj.title}<br><sup>{plot_obj.error_msg}</sup>")
    fig.add_trace(
        go.Scatter(
            x=x_reads,
            y=plot_obj.y_data,
            mode="lines",
            name="Observed data",
            customdata=np.column_stack((y_cpgs, plot_obj.x_data)),
            hovertemplate=(
                "<b>Observed</b><br>"
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Downsampling: %{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    fig.write_html(plot_obj.output_path)
    print(f"⚠️ Curve fitting failed but plot saved anyway to: {plot_obj.output_path}.")


def plot_fitted_data(plot_obj):
    """Plot observed and predicted CpG values based on fitted asymptotic growth."""
    # Extended x-data for predictions
    x_all = np.append(plot_obj.x_data, np.linspace(1.2, 2.0, 5))
    y_all = asymptotic_growth(x_all, *plot_obj.params)

    reads_all = [x * plot_obj.reads for x in x_all]
    reads_fmt = fmt_list(reads_all)
    cpgs_fmt = fmt_list(y_all)
    saturation = np.round((y_all / plot_obj.asymptote) * 100, 1)

    n_obs = len(plot_obj.x_data) - 1

    obs = slice(None, n_obs + 2)
    pred = slice(n_obs + 1, None)
    fig = make_base_plot(plot_obj.title)

    # Observed
    fig.add_trace(
        go.Scatter(
            x=reads_fmt[obs],
            y=y_all[obs],
            mode="lines",
            name="Observed data",
            customdata=np.column_stack((cpgs_fmt[obs], saturation[obs], x_all[obs])),
            hovertemplate=(
                "<b>Observed</b><br>"
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Saturation: %{customdata[1]}%<br>"
                "Downsampling: %{customdata[2]}"
                "<extra></extra>"
            ),
            line=dict(color="#1f77b4"),
        )
    )

    # Predicted
    fig.add_trace(
        go.Scatter(
            x=reads_fmt[pred],
            y=y_all[pred],
            mode="lines",
            name="Predicted data",
            customdata=np.column_stack((cpgs_fmt[pred], saturation[pred])),
            hovertemplate=(
                "<b>Predicted</b><br>"
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Saturation: %{customdata[1]}%"
                "<extra></extra>"
            ),
            line=dict(color="#1f77b4"),
        )
    )

    # Asymptote line
    cpgs_found_index = len(plot_obj.x_data) - 1
    asympt_sat = round((y_all[cpgs_found_index] / plot_obj.asymptote) * 100, 1)
    fig.add_hline(
        y=plot_obj.asymptote,
        line_dash="dash",
        annotation_text=(
            f"Asymptote = {human_readable(plot_obj.asymptote)} CpGs "
            f"(Saturation = {asympt_sat}%)"
        ),
        annotation_position="top right",
        annotation_yshift=10,  # push slightly above
    )

    fig.write_html(plot_obj.output_path)
    print(f"✅ Plot saved to: {plot_obj.output_path}")
