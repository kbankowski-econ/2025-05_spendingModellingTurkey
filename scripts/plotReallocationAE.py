"""
Figure 13, panel 1: AE expenditure reallocation.

Grouped bar chart of advanced-economy output response (yd, % deviation from
baseline) to three expenditure-reallocation shocks, at four horizons.

Shocks:
  - Infrastructure investment -> Model_HumanCapital_epsi_ig
  - Human capital investment  -> Model_HumanCapital_epsi_cge
  - R&D spending              -> Model_HumanCapital_epsi_cgrd

The script reads the reduced annual export and writes chart files and plotted
data to results/figure13/figures.
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from wp_charts import chart_render_px, chart_display_cm, font_px_for_pt, smart_save_image, write_pdf

# --- Paths (resolved from this file; the data CSV is the only external input) -
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_CSV = PROJECT_ROOT / "data" / "figure13_yearly.csv"
FIGURES_DIR = PROJECT_ROOT / "results" / "figure13" / "figures"

# --- Styling (inlined from the former chartConfig.json) -----------------------
STYLE = {
    "template": "simple_white",
    "font_size": 22,
    "margins": {"t": 40, "b": 30, "l": 25, "r": 25},  # snug to the legend
    "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02,
               "xanchor": "center", "x": 0.5, "font_size": 14},
    "axes": {"linecolor": "black", "linewidth": 1.5, "ticks": "inside",
             "showgrid": True, "gridcolor": "rgba(0,0,0,0.15)", "gridwidth": 0.5,
             "zeroline": True, "zerolinewidth": 1.5, "tickfont_size": 16},
}

SERIES = [
    ("Model_HumanCapital_epsi_ig___yd",    "Infrastructure investment", "#1565C0"),
    ("Model_HumanCapital_epsi_cge___yd",   "Human capital investment",  "#6A1B9A"),
    ("Model_HumanCapital_epsi_cgrd___yd",  "R&D spending",              "#2E7D32"),
]

YEARS = [2026, 2030, 2040, 2050]
# Convention: first label as full yyyy, the rest as two-digit yy.
YEAR_LABELS = [str(YEARS[0])] + [f"{y % 100:02d}" for y in YEARS[1:]]
OUTPUT_STEM = "reallocationAE_yd"

# Both sizes come from chartTable.csv: render = original chart size (canvas,
# controls fonts/quality); display = size shown in the paper (aspect preserved).
WIDTH_PX, HEIGHT_PX = chart_render_px(OUTPUT_STEM, (14.82, 9.53))
DISPLAY_CM = chart_display_cm(OUTPUT_STEM, (14.82, 9.53))

# Font matching the paper: Palatino (the paper's mathpazo) sized to the paper's
# 11pt body. FONT_PX is recomputed from the render/display sizes, so the text
# stays 11pt on the page however the chart is resized.
TARGET_FONT_PT = 8
FONT_FAMILY = "Palatino, 'Palatino Linotype', 'Book Antiqua', serif"
FONT_PX = font_px_for_pt(TARGET_FONT_PT, WIDTH_PX, DISPLAY_CM[0])
LEGEND_FONT_PT = 7  # legend smaller than the 8pt tick labels
LEGEND_FONT_PX = font_px_for_pt(LEGEND_FONT_PT, WIDTH_PX, DISPLAY_CM[0])


def load_data():
    df = pd.read_csv(INPUT_CSV)
    df = df.rename(columns={df.columns[0]: "date"})
    df["year"] = df["date"].str.extract(r"(\d{4})").astype(int)
    return df


def main():
    df = load_data()
    df = df[df["year"].isin(YEARS)].sort_values("year")

    fig = go.Figure()
    for col, label, color in SERIES:
        fig.add_trace(
            go.Bar(
                x=YEAR_LABELS,
                y=df.set_index("year").loc[YEARS, col].values,
                name=label,
                marker_color=color,
            )
        )

    fig.update_layout(
        template=STYLE["template"],
        width=WIDTH_PX,
        height=HEIGHT_PX,
        margin=STYLE["margins"],
        font=dict(family=FONT_FAMILY, size=FONT_PX),
        barmode="group",
        bargap=0.2,
        bargroupgap=0.05,
        legend=dict(
            orientation=STYLE["legend"]["orientation"],
            yref="container", yanchor="top", y=0.99,  # pin to figure top, no blank band
            xanchor=STYLE["legend"]["xanchor"],
            x=STYLE["legend"]["x"],
            font=dict(size=LEGEND_FONT_PX),
        ),
    )

    axes = STYLE["axes"]
    fig.update_xaxes(
        showgrid=False,
        linecolor=axes["linecolor"],
        linewidth=axes["linewidth"],
        ticks=axes["ticks"],
        tickfont=dict(size=FONT_PX),
        title=None,
    )
    fig.update_yaxes(
        showgrid=axes["showgrid"],
        gridcolor=axes["gridcolor"],
        gridwidth=axes["gridwidth"],
        zeroline=axes["zeroline"],
        zerolinewidth=axes["zerolinewidth"],
        zerolinecolor="black",
        linecolor=axes["linecolor"],
        linewidth=axes["linewidth"],
        ticks=axes["ticks"],
        tickfont=dict(size=FONT_PX),
        title=None,
    )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    png_path = FIGURES_DIR / f"{OUTPUT_STEM}.png"
    pdf_path = FIGURES_DIR / f"{OUTPUT_STEM}.pdf"
    html_path = FIGURES_DIR / f"{OUTPUT_STEM}.html"
    smart_save_image(fig, png_path, DISPLAY_CM)
    write_pdf(fig, pdf_path, WIDTH_PX, DISPLAY_CM[0])  # vector PDF at the display size
    fig.write_html(html_path, auto_open=False)
    print(f"  Saved {png_path.name}, {pdf_path.name} and {html_path.name}")

    csv_cols = ["year"] + [c for c, _, _ in SERIES]
    csv_data = df[csv_cols].copy()
    rename_map = {c: label for c, label, _ in SERIES}
    csv_data = csv_data.rename(columns=rename_map).round(3)
    csv_path = FIGURES_DIR / f"{OUTPUT_STEM}.csv"
    csv_data.to_csv(csv_path, index=False)
    print(f"  Exported data to {csv_path.name}")


if __name__ == "__main__":
    main()
