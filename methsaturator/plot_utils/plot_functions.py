import numpy as np
from rich.console import Console
from .math_model import asymptotic_growth
import plotly.graph_objs as go

# ===============================================================
# Plotting Functions
# ===============================================================

console = Console()


def human_readable(num):
    if num >= 1e9:
        return f"{num/1e9:.1f}B"
    elif num >= 1e6:
        return f"{num/1e6:.1f}M"
    elif num >= 1e3:
        return f"{num/1e3:.1f}K"
    else:
        return str(int(num))


def plot_fallback(plot_obj):
    # Extend x-axis for predicted values
    number_reads = [x * plot_obj.reads for x in plot_obj.x_data]
    number_reads = [human_readable(round(x, 0)) for x in number_reads]
    number_cpgs = [human_readable(round(x, 0)) for x in plot_obj.y_data]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=number_reads,
            y=plot_obj.y_data,
            mode="lines",
            name="Observed data",
            customdata=np.column_stack((number_cpgs, plot_obj.x_data)),
            hovertemplate=(
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Downsampling: %{customdata[1]}"
                "<extra></extra>"
            ),
        )
    )

    # Axes
    fig.update_xaxes(title_text="Number of reads", showgrid=True)
    fig.update_yaxes(title_text="Number of CpGs", showgrid=True)
    fig.update_layout(
        title=dict(
            text=f"{plot_obj.title}<br><sup>{plot_obj.error_msg}</sup>", x=0.5, y=0.9
        ),
        width=950,
        height=620,
        template="plotly_white",
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
    )

    html_path = plot_obj.output_path.replace(".svg", ".html")
    fig.write_html(html_path)
    print(f"⚠️ Curve fitting failed but plot saved anyway to: {html_path}.")


def plot_fitted_data(plot_obj):
    """
    Predict theorical number of CpGs given the parameters of the fitted curve.
    Here we use the percentage as the explanatory variable, reason why we use
    increased subsampling percentage to predict the number of CpGs. However,
    we could also use the number of reads.
    """
    # Calculate the theoretical number CpGs
    downsampling_percentages = np.append(
        plot_obj.x_data, np.array([1.2, 1.4, 1.6, 1.8, 2.0])
    )
    number_cpgs = asymptotic_growth(downsampling_percentages, *plot_obj.params)

    # Calculate the number of reads corresponding to increased percentage
    # multiplying each percentage for the number of reads at percentage==1,
    # that is on the raw, not downsampled bam file
    number_reads = [x * plot_obj.reads for x in downsampling_percentages]
    number_reads = [human_readable(round(x, 0)) for x in number_reads]

    # Calculate the saturation % at each percentage
    saturation_values = [
        round((number_cpgs[i] / plot_obj.asymptote) * 100, 0)
        for i in range(len(number_cpgs))
    ]

    # Divide into predicted and observed values to show them in the plot
    predicted_cpgs = number_cpgs[len(plot_obj.x_data) :]
    human_read_predicted_cpgs = [human_readable(round(x, 0)) for x in predicted_cpgs]
    observed_cpgs = number_cpgs[: len(plot_obj.x_data) + 1]
    human_read_observed_cpgs = [human_readable(round(x, 0)) for x in observed_cpgs]
    predicted_reads = number_reads[len(plot_obj.x_data) :]
    observed_reads = number_reads[: len(plot_obj.x_data) + 1]
    predicted_saturation = saturation_values[len(plot_obj.x_data) :]
    observed_saturation = saturation_values[: len(plot_obj.x_data) + 1]
    observed_percentages = downsampling_percentages[: len(plot_obj.x_data) + 1]

    # Plot the observed data points
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=observed_reads,
            y=observed_cpgs,
            mode="lines",
            name="Observed data",
            customdata=np.column_stack(
                (human_read_observed_cpgs, observed_saturation, observed_percentages)
            ),
            hovertemplate=(
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Saturation: %{customdata[1]}%<br>"
                "Downsampling: %{customdata[2]}"
                "<extra></extra>"
            ),
        )
    )

    # Predicted data points
    fig.add_trace(
        go.Scatter(
            x=predicted_reads,
            y=predicted_cpgs,
            mode="lines+markers",
            name="Predicted data",
            customdata=np.column_stack(
                (human_read_predicted_cpgs, predicted_saturation)
            ),
            hovertemplate=(
                "Number of reads: %{x}<br>"
                "Number CpGs: %{customdata[0]}<br>"
                "Saturation: %{customdata[1]}%"
                "<extra></extra>"
            ),
            line=dict(dash="dash"),
        )
    )

    # Asymptote
    asympt_formatted = human_readable(plot_obj.asymptote)
    fig.add_hline(
        y=plot_obj.asymptote,
        line_dash="dash",
        annotation_text=f"Asymptote = {asympt_formatted} CpGs",
        annotation_position="bottom right",
    )

    # Axes
    fig.update_xaxes(title_text="Number of reads", showgrid=True)
    fig.update_yaxes(title_text="Number of CpGs", showgrid=True)

    fig.update_layout(
        title=dict(text=plot_obj.title, x=0.5, y=0.9),
        width=950,
        height=620,
        template="plotly_white",
        legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99),
    )

    html_path = plot_obj.output_path.replace(".svg", ".html")
    fig.write_html(html_path)
    print(f"✅ Plot saved to: {html_path}")
