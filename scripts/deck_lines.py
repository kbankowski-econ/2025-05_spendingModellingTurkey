"""
Shared renderer for the Türkiye deck's line panels.

Each of the deck's three chart slides shows the same chart for three
calibrations (advanced economies, EMDEs, Türkiye), so the panels have to be
directly comparable: the same styling, and one y-range shared across the three.
A slide is described by a `Slide` and rendered by `render_slide`, which writes a
PNG, a vector PDF, an HTML copy, and the plotted data for every panel.

Colors follow the entity throughout the deck and the paper: blue for
infrastructure, purple for human capital, green for R&D. Closure speed is
carried by the dash style, so no series is identified by color alone.
"""
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from wp_charts import chart_render_px, chart_display_cm, font_px_for_pt, smart_save_image, write_pdf

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_CSV = PROJECT_ROOT / "data" / "figure13_yearly.csv"
FIGURES_DIR = PROJECT_ROOT / "results" / "turkiye" / "figures"

INFRA, HUMAN_CAPITAL, RD = "#1565C0", "#6A1B9A", "#2E7D32"
LEGEND_GREY = "#757575"

FIRST_YEAR = 2025
LAST_YEAR = 2050
# Horizons carried over from the Figure 13 bar charts. Only the final year is
# labelled: a number on every marker of every series is unreadable at three
# panels to a slide.
MARK_YEARS = [2026, 2030, 2040, 2050]
# Convention: first label as full yyyy, the rest as two-digit yy.
TICK_YEARS = [2030, 2035, 2040, 2045, 2050]
TICK_LABELS = [str(TICK_YEARS[0])] + [f"{y % 100:02d}" for y in TICK_YEARS[1:]]

STYLE = {
    "template": "simple_white",
    "margins": {"t": 40, "b": 30, "l": 25, "r": 25},
    "axes": {"linecolor": "black", "linewidth": 1.5, "ticks": "inside",
             "showgrid": True, "gridcolor": "rgba(0,0,0,0.15)", "gridwidth": 0.5,
             "zeroline": True, "zerolinewidth": 1.5},
    "line_width": 2,
}

# Default render/display sizes for a three-to-a-slide panel; chartTable.csv
# overrides them per figure.
DEFAULT_CM = (9.0, 6.5)
DEFAULT_DISPLAY_CM = (4.5, 3.25)

# Smaller than the paper's 8pt: three panels to a slide leave each one about a
# third of the text width.
TARGET_FONT_PT = 7
LEGEND_FONT_PT = 6
# Minimum gap between two endpoint value labels, as a multiple of their font
# size: the label box is roughly one line plus padding.
LABEL_GAP_LINES = 1.8
# Sans, to sit with the deck, which keeps beamer's default Latin Modern Sans.
# That font ships with TeX Live rather than as a system font, so the browser
# engine behind the renderer falls back to Helvetica unless it is installed; the
# charts stay sans either way. The paper's charts are unaffected and keep its
# Palatino body text.
FONT_FAMILY = "'Latin Modern Sans', 'CMU Sans Serif', Helvetica, Arial, sans-serif"

# Background of the endpoint value labels. The sensitivity panels use green so
# that a slide built on alternative efficiency-gap estimates is recognisable at
# a glance, next to the yellow of the main results.
LABEL_BG = "#FFF9C4"
LABEL_BG_SENSITIVITY = "#DCEDC8"


@dataclass
class Series:
    """One line. `base` makes the line a difference from that column."""
    label: str
    col: str
    color: str
    dash: str = "solid"
    base: str | None = None
    label_yshift: int = 0


@dataclass
class Panel:
    stem: str          # output file stem, e.g. "reallocationTR_yd_lines"
    series: list[Series]
    # Override the slide's legends. The advanced-economy panels have no
    # 2040-closure experiment, so they must not advertise one, and they carry an
    # R&D line the other panels lack.
    dash_legend: list[tuple[str, str]] | None = None
    color_legend: list[tuple[str, str]] | None = None
    label_bgcolor: str = LABEL_BG


@dataclass
class Slide:
    panels: list[Panel]
    # Extra legend entries drawn in grey to explain the dash styles. Colors are
    # explained by the color legend built from the series labels.
    dash_legend: list[tuple[str, str]] = field(default_factory=list)
    # Series labels to show in the color legend, in order. Empty means every
    # distinct (label, color) pair in the panel.
    color_legend: list[tuple[str, str]] = field(default_factory=list)


def load_data():
    df = pd.read_csv(INPUT_CSV)
    df = df.rename(columns={df.columns[0]: "date"})
    df["year"] = df["date"].str.extract(r"(\d{4})").astype(int)
    df = df[(df["year"] >= FIRST_YEAR) & (df["year"] <= LAST_YEAR)]
    return df.sort_values("year")


def _values(df, series: Series):
    if series.base is None:
        return df[series.col]
    return df[series.col] - df[series.base]


def shared_range(df, slide: Slide, pad_bottom=0.05, pad_top=0.20):
    """One y-range covering every panel, so the slide's three panels can be read
    against each other. The generous top padding is headroom for the stack of
    endpoint value labels."""
    lo, hi = 0.0, 0.0
    for panel in slide.panels:
        for series in panel.series:
            values = _values(df, series)
            lo, hi = min(lo, values.min()), max(hi, values.max())
    span = hi - lo
    return [lo - pad_bottom * span, hi + pad_top * span]


def color_legend_labels(panel: Panel, slide: Slide):
    return panel.color_legend or slide.color_legend or list(
        dict.fromkeys((s.label, s.color) for s in panel.series)
    )


def dash_legend_labels(panel: Panel, slide: Slide):
    return panel.dash_legend if panel.dash_legend is not None else slide.dash_legend


def _legend_height_px(color_entries, dash_entries, width_px, font_px):
    """Height the horizontal legend will take. Panels are narrow enough that the
    legend wraps onto several rows, and it is subtracted from the plot area
    before the value labels are spaced -- otherwise they are spread over a plot
    that is half the height assumed and overprint each other."""
    labels = [label for label, _ in color_entries] + [label for label, _ in dash_entries]
    if not labels:
        return 0
    swatch_px = 2.8 * font_px          # line sample plus its padding
    rows, row_used = 1, 0.0
    for label in labels:
        entry = swatch_px + 0.52 * font_px * len(label)
        if row_used and row_used + entry > width_px:
            rows, row_used = rows + 1, entry
        else:
            row_used += entry
    return rows * font_px * 1.7


def _label_positions(endpoints, yrange, plot_height_px, font_px):
    """Vertical positions for the endpoint value labels: the value itself where
    labels are far enough apart, nudged upwards in ascending order where they
    would otherwise overprint. Several scenarios end within a few tenths of each
    other, so this collision pass is what keeps the numbers readable. The whole
    stack is shifted back down if it would run past the top of the axis."""
    span = yrange[1] - yrange[0]
    min_gap = span * (LABEL_GAP_LINES * font_px) / max(plot_height_px, 1)

    positions = {}
    previous = None
    for key, value in sorted(endpoints.items(), key=lambda item: item[1]):
        position = value if previous is None else max(value, previous + min_gap)
        positions[key] = position
        previous = position

    overshoot = (previous or yrange[1]) - (yrange[1] - min_gap / 2)
    if overshoot > 0:
        positions = {key: value - overshoot for key, value in positions.items()}
    return positions


def _render_panel(df, panel: Panel, slide: Slide, yrange):
    width_px, height_px = chart_render_px(panel.stem, DEFAULT_CM)
    display_cm = chart_display_cm(panel.stem, DEFAULT_DISPLAY_CM)
    font_px = font_px_for_pt(TARGET_FONT_PT, width_px, display_cm[0])
    legend_font_px = font_px_for_pt(LEGEND_FONT_PT, width_px, display_cm[0])

    fig = go.Figure()
    marks = df[df["year"].isin(MARK_YEARS)]
    last_year = df["year"].max()

    plot_height_px = (
        height_px
        - STYLE["margins"]["t"]
        - STYLE["margins"]["b"]
        - _legend_height_px(color_legend_labels(panel, slide), dash_legend_labels(panel, slide),
                            width_px, legend_font_px)
    )
    endpoints = {
        index: _values(df, series)[df["year"] == last_year].iloc[0]
        for index, series in enumerate(panel.series)
    }
    label_y = _label_positions(endpoints, yrange, plot_height_px, legend_font_px)

    for index, series in enumerate(panel.series):
        values = _values(df, series)
        fig.add_trace(
            go.Scatter(
                x=df["year"], y=values, name=series.label, mode="lines",
                line=dict(color=series.color, width=STYLE["line_width"], dash=series.dash),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=marks["year"], y=_values(marks, series), mode="markers",
                marker=dict(color=series.color, size=8),
                showlegend=False, hoverinfo="skip",
            )
        )
        fig.add_annotation(
            x=last_year, y=label_y[index], text=f"{endpoints[index]:.1f}", showarrow=False,
            xshift=16, yshift=series.label_yshift,
            font=dict(size=legend_font_px, color=series.color),
            bgcolor=panel.label_bgcolor, borderpad=2,
        )

    # Legends are drawn as empty traces so their swatches carry the same line
    # style as the data.
    for label, color in color_legend_labels(panel, slide):
        fig.add_trace(
            go.Scatter(x=[None], y=[None], name=label, mode="lines",
                       line=dict(color=color, width=STYLE["line_width"]), showlegend=True)
        )
    for label, dash in dash_legend_labels(panel, slide):
        fig.add_trace(
            go.Scatter(x=[None], y=[None], name=label, mode="lines",
                       line=dict(color=LEGEND_GREY, width=STYLE["line_width"], dash=dash),
                       showlegend=True)
        )

    fig.update_layout(
        template=STYLE["template"], width=width_px, height=height_px,
        margin=STYLE["margins"],
        font=dict(family=FONT_FAMILY, size=font_px),
        legend=dict(orientation="h", yref="container", yanchor="top", y=0.99,
                    xanchor="center", x=0.5, font=dict(size=legend_font_px)),
    )

    axes = STYLE["axes"]
    fig.update_xaxes(
        range=[FIRST_YEAR, LAST_YEAR + 2], showgrid=False,
        linecolor=axes["linecolor"], linewidth=axes["linewidth"], ticks=axes["ticks"],
        tickfont=dict(size=font_px), tickvals=TICK_YEARS, ticktext=TICK_LABELS, title=None,
    )
    fig.update_yaxes(
        range=yrange, showgrid=axes["showgrid"], gridcolor=axes["gridcolor"],
        gridwidth=axes["gridwidth"], zeroline=axes["zeroline"],
        zerolinewidth=axes["zerolinewidth"], zerolinecolor="black",
        linecolor=axes["linecolor"], linewidth=axes["linewidth"], ticks=axes["ticks"],
        tickfont=dict(size=font_px), title=None,
    )
    return fig, width_px, display_cm


def render_slide(slide: Slide):
    df = load_data()
    yrange = shared_range(df, slide)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    for panel in slide.panels:
        fig, width_px, display_cm = _render_panel(df, panel, slide, yrange)

        png_path = FIGURES_DIR / f"{panel.stem}.png"
        pdf_path = FIGURES_DIR / f"{panel.stem}.pdf"
        html_path = FIGURES_DIR / f"{panel.stem}.html"
        smart_save_image(fig, png_path, display_cm)
        write_pdf(fig, pdf_path, width_px, display_cm[0])
        fig.write_html(html_path, auto_open=False)
        print(f"  Saved {png_path.name}, {pdf_path.name} and {html_path.name}")

        plotted = pd.DataFrame({"year": df["year"].values})
        for series in panel.series:
            plotted[series.label] = _values(df, series).round(3).values
        csv_path = FIGURES_DIR / f"{panel.stem}.csv"
        plotted.to_csv(csv_path, index=False)
        print(f"  Exported data to {csv_path.name}")
