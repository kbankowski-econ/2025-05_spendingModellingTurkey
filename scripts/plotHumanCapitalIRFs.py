"""
Figure 13, panel 5: human capital and R&D policy mix.

Line chart of the aggregate output response (yd, % deviation) for three
human-capital related spending shocks.

Series:
  - Model_HumanCapital_epsi_cgeCgrd___yd  (Joint human capital + R&D)
  - Model_HumanCapital_epsi_cge___yd      (Human capital investment)
  - Model_HumanCapital_epsi_cgrd___yd     (R&D investment)

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
    "line_width_standard": 2.5,
}

SERIES = [
    ("Model_HumanCapital_epsi_cgeCgrd___yd",  "Joint human capital + R&D", "#E65100"),
    ("Model_HumanCapital_epsi_cge___yd",      "Human capital investment",  "#6A1B9A"),
    ("Model_HumanCapital_epsi_cgrd___yd",     "R&D investment",            "#2E7D32"),
]

PLOT_START_YEAR = 2026
X_TICKS = [2026, 2031, 2036, 2041, 2046, 2050]
# Show the first tick as full 4-digit year, abbreviate the rest to 2 digits.
X_TICK_LABELS = [str(X_TICKS[0])] + [f"{y % 100:02d}" for y in X_TICKS[1:]]
OUTPUT_STEM = "humanCapital_yd_IRF"

# Both sizes come from chartTable.csv: render = original chart size (canvas,
# controls fonts/quality); display = size shown in the paper (aspect preserved).
WIDTH_PX, HEIGHT_PX = chart_render_px(OUTPUT_STEM, (14.82, 9.53))
DISPLAY_CM = chart_display_cm(OUTPUT_STEM, (14.82, 9.53))

# Font matching the paper: Palatino (the paper's mathpazo), sized so the chart
# text renders at a fixed point size on the page (recomputed from render/display).
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
    df = df[df["year"] >= PLOT_START_YEAR]

    fig = go.Figure()
    for col, label, color in SERIES:
        fig.add_trace(
            go.Scatter(
                x=df["year"],
                y=df[col],
                mode="lines",
                name=label,
                line=dict(color=color, width=STYLE["line_width_standard"]),
            )
        )

    fig.update_layout(
        template=STYLE["template"],
        width=WIDTH_PX,
        height=HEIGHT_PX,
        margin=STYLE["margins"],
        font=dict(family=FONT_FAMILY, size=FONT_PX),
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
        showgrid=axes["showgrid"],
        gridcolor=axes["gridcolor"],
        gridwidth=axes["gridwidth"],
        linecolor=axes["linecolor"],
        linewidth=axes["linewidth"],
        ticks=axes["ticks"],
        tickfont=dict(size=FONT_PX),
        tickmode="array",
        tickvals=X_TICKS,
        ticktext=X_TICK_LABELS,
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
