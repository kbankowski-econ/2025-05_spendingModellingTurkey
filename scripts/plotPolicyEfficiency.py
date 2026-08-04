"""Figure 13, panels 3 and 4: spending-efficiency reforms."""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from wp_charts import (
    chart_display_cm,
    chart_render_px,
    font_px_for_pt,
    smart_save_image,
    write_pdf,
)


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_CSV = PROJECT_ROOT / "data" / "figure13_yearly.csv"
FIGURES_DIR = PROJECT_ROOT / "results" / "figure13" / "figures"
TARGET_YEAR = 2050
FONT_FAMILY = "Palatino, 'Palatino Linotype', 'Book Antiqua', serif"

STYLE = {
    "template": "simple_white",
    "margins": {"t": 24, "b": 24, "l": 34, "r": 8},
    "axes": {
        "linecolor": "black",
        "linewidth": 1.5,
        "ticks": "inside",
        "showgrid": True,
        "gridcolor": "rgba(0,0,0,0.15)",
        "gridwidth": 0.5,
        "zeroline": True,
        "zerolinewidth": 1.5,
    },
}

AE_SERIES = [
    (
        "Infrastructure<br>investment",
        "Model_HumanCapital_epsi_igeff25y___yd",
        "Model_HumanCapital_epsi_ig___yd",
        "#1565C0",
    ),
    (
        "Human capital<br>investment",
        "Model_HumanCapital_epsi_cgeeff25y___yd",
        "Model_HumanCapital_epsi_cge___yd",
        "#6A1B9A",
    ),
    (
        "R&D<br>spending",
        "Model_HumanCapital_epsi_cgrd_eff25y___yd",
        "Model_HumanCapital_epsi_cgrd___yd",
        "#2E7D32",
    ),
]

EMDE_SUBPLOTS = [
    {
        "title": "Infrastructure investment",
        "color": "#1565C0",
        "scenarios": [
            (
                "by 2050",
                "EM_Model_HumanCapital_epsiigeff25y___yd",
                "EM_Model_HumanCapital_epsiig___yd",
                "EM_Model_HumanCapital_epsiigeff25ylow___yd",
                "EM_Model_HumanCapital_epsiiglow___yd",
            ),
            (
                "by 2040",
                "EM_Model_HumanCapital_epsiigeff30y___yd",
                "EM_Model_HumanCapital_epsiig___yd",
                "EM_Model_HumanCapital_epsiigeff30ylow___yd",
                "EM_Model_HumanCapital_epsiiglow___yd",
            ),
        ],
    },
    {
        "title": "Human capital investment",
        "color": "#6A1B9A",
        "scenarios": [
            (
                "by 2050",
                "EM_Model_HumanCapital_epsicgeeff25y___yd",
                "EM_Model_HumanCapital_epsicge___yd",
                "EM_Model_HumanCapital_epsicgeeff25ylow___yd",
                "EM_Model_HumanCapital_epsicgelow___yd",
            ),
            (
                "by 2040",
                "EM_Model_HumanCapital_epsicgeeff30y___yd",
                "EM_Model_HumanCapital_epsicge___yd",
                "EM_Model_HumanCapital_epsicgeeff30ylow___yd",
                "EM_Model_HumanCapital_epsicgelow___yd",
            ),
        ],
    },
]

BAR_NAME = "Closing the gap in the baseline"
MARKER_NAME = "Efficiency improvement from a higher initial gap"


def load_target_row():
    df = pd.read_csv(INPUT_CSV)
    df = df.rename(columns={df.columns[0]: "date"})
    df["year"] = df["date"].str.extract(r"(\d{4})").astype(int)
    return df[df["year"] == TARGET_YEAR].iloc[0]


def output_paths(output_stem):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    return (
        FIGURES_DIR / f"{output_stem}.png",
        FIGURES_DIR / f"{output_stem}.pdf",
        FIGURES_DIR / f"{output_stem}.html",
        FIGURES_DIR / f"{output_stem}.csv",
    )


def save_figure(fig, output_stem, width_px, display_cm, csv_data):
    png_path, pdf_path, html_path, csv_path = output_paths(output_stem)
    smart_save_image(fig, png_path, display_cm)
    write_pdf(fig, pdf_path, width_px, display_cm[0])
    fig.write_html(html_path, auto_open=False)
    csv_data.to_csv(csv_path, index=False)
    print(f"  Saved {png_path.name}, {pdf_path.name}, {html_path.name}, and CSV data")


def apply_axes(fig, font_px):
    axes = STYLE["axes"]
    fig.update_xaxes(
        showgrid=False,
        linecolor=axes["linecolor"],
        linewidth=axes["linewidth"],
        ticks=axes["ticks"],
        tickfont=dict(size=font_px),
        title=None,
    )
    fig.update_yaxes(
        rangemode="tozero",
        showgrid=axes["showgrid"],
        gridcolor=axes["gridcolor"],
        gridwidth=axes["gridwidth"],
        zeroline=axes["zeroline"],
        zerolinewidth=axes["zerolinewidth"],
        zerolinecolor="black",
        linecolor=axes["linecolor"],
        linewidth=axes["linewidth"],
        ticks=axes["ticks"],
        tickfont=dict(size=font_px),
        title=None,
    )


def plot_ae(row):
    output_stem = "policyEfficiencyAE_yd"
    width_px, height_px = chart_render_px(output_stem, (7.5, 5.0))
    display_cm = chart_display_cm(output_stem, (7.5, 5.0))
    font_px = font_px_for_pt(7, width_px, display_cm[0])

    bars = [
        (label, row[efficiency] - row[baseline], color)
        for label, efficiency, baseline, color in AE_SERIES
    ]

    fig = go.Figure(
        go.Bar(
            x=[item[0] for item in bars],
            y=[item[1] for item in bars],
            marker_color=[item[2] for item in bars],
            showlegend=False,
        )
    )
    fig.update_layout(
        template=STYLE["template"],
        width=width_px,
        height=height_px,
        margin=STYLE["margins"],
        font=dict(family=FONT_FAMILY, size=font_px),
        bargap=0.35,
    )
    apply_axes(fig, font_px)

    csv_data = pd.DataFrame(
        {
            "category": [item[0].replace("<br>", " ") for item in bars],
            "additional_gain_2050": [round(item[1], 3) for item in bars],
        }
    )
    save_figure(fig, output_stem, width_px, display_cm, csv_data)


def plot_emde(row):
    output_stem = "policyEfficiencyEM_yd"
    width_px, height_px = chart_render_px(output_stem, (7.5, 5.0))
    display_cm = chart_display_cm(output_stem, (7.5, 5.0))
    font_px = font_px_for_pt(6.5, width_px, display_cm[0])
    legend_font_px = font_px_for_pt(6.2, width_px, display_cm[0])
    title_font_px = font_px_for_pt(6.5, width_px, display_cm[0])

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[subplot["title"] for subplot in EMDE_SUBPLOTS],
        horizontal_spacing=0.19,
    )
    records = []
    for col, subplot in enumerate(EMDE_SUBPLOTS, start=1):
        labels = [scenario[0] for scenario in subplot["scenarios"]]
        baseline_values = [
            row[scenario[1]] - row[scenario[2]]
            for scenario in subplot["scenarios"]
        ]
        higher_gap_values = [
            row[scenario[3]] - row[scenario[4]]
            for scenario in subplot["scenarios"]
        ]
        color = subplot["color"]

        fig.add_trace(
            go.Bar(
                x=labels,
                y=baseline_values,
                marker_color=color,
                showlegend=False,
            ),
            row=1,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=labels,
                y=higher_gap_values,
                mode="markers",
                marker=dict(symbol="circle", size=10, color=color),
                showlegend=False,
            ),
            row=1,
            col=col,
        )

        for label, baseline_value, higher_gap_value in zip(
            labels, baseline_values, higher_gap_values
        ):
            records.append(
                {
                    "instrument": subplot["title"],
                    "closure_horizon": label,
                    "calibrated_gap": round(baseline_value, 3),
                    "higher_initial_gap": round(higher_gap_value, 3),
                }
            )

    neutral = "#757575"
    fig.add_trace(
        go.Bar(
            x=[None],
            y=[None],
            marker_color=neutral,
            name=BAR_NAME,
            showlegend=True,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="circle", size=10, color=neutral),
            name=MARKER_NAME,
            showlegend=True,
        ),
        row=1,
        col=1,
    )

    for annotation in fig.layout.annotations:
        annotation.font = dict(family=FONT_FAMILY, size=title_font_px)
        annotation.y += 0.07

    fig.update_layout(
        template=STYLE["template"],
        width=width_px,
        height=height_px,
        margin={"t": 72, "b": 35, "l": 34, "r": 8},
        font=dict(family=FONT_FAMILY, size=font_px),
        bargap=0.45,
        legend=dict(
            orientation="h",
            yref="container",
            yanchor="top",
            y=0.99,
            xanchor="center",
            x=0.5,
            font=dict(size=legend_font_px),
        ),
    )
    apply_axes(fig, font_px)
    save_figure(
        fig,
        output_stem,
        width_px,
        display_cm,
        pd.DataFrame(records),
    )


def main():
    row = load_target_row()
    plot_ae(row)
    plot_emde(row)


if __name__ == "__main__":
    main()
