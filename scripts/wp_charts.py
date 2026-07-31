"""
Shared helpers for the Figure 13 chart scripts in this folder.

  - chart_render_px:  read a chart's *render* (original) size (cm) -> pixels
  - chart_display_cm: read a chart's *display* size (cm) shown in the paper
  - smart_save_image: write a PNG, tagged so its natural size in LaTeX equals the
                      requested display size, only when its bytes change

Both sizes live in chartTable.csv. RenderWidth/RenderHeight set the plotly canvas
(hence font sizes and resolution); DisplayWidth/DisplayHeight set the size the
figure appears at in the paper, applied via a DPI tag so a bare \\includegraphics
renders it there. The two are independent: shrink DisplayWidth to make a figure
smaller in the paper without touching its fonts. chartTable.csv is expected
alongside this module. Depends only on the standard library and plotly.
"""
import struct
import zlib
from pathlib import Path

import plotly.io as pio

_THIS_DIR = Path(__file__).resolve().parent
CONFIG_CSV = _THIS_DIR / "chartTable.csv"
_CM_PER_INCH = 2.54
_CM_TO_PX = 37.795275591  # 1 cm at 96 DPI (the render canvas's logical DPI)
_PT_PER_INCH = 72.27       # TeX points per inch (LaTeX's "pt")


def font_px_for_pt(target_pt, render_width_px, display_width_cm):
    """Canvas font size (px) so chart text renders at `target_pt` points on the
    page, given the render width (px) and the on-page display width (cm). Keeps
    figure text at a fixed point size however the chart is scaled into the paper:
    a chart shown at half its render width needs double the canvas font px."""
    render_width_cm = render_width_px / _CM_TO_PX
    return round(target_pt * (96.0 / _PT_PER_INCH) * render_width_cm / display_width_cm, 1)


def _read_cm(stem, width_col, height_col, default_cm):
    """Read a (width_cm, height_cm) pair from chartTable.csv by matching pngFile.
    Falls back to default_cm if the file, row, or columns are missing/blank."""
    import csv
    width_cm, height_cm = default_cm
    if CONFIG_CSV.exists():
        with CONFIG_CSV.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if Path(row.get("pngFile", "")).name == f"{stem}.png":
                    if row.get(width_col) and row.get(height_col):
                        width_cm, height_cm = float(row[width_col]), float(row[height_col])
                    break
    return width_cm, height_cm


def chart_render_px(stem, default_cm):
    """Original chart (render canvas) size in pixels, from RenderWidth/RenderHeight
    (cm) in chartTable.csv. This is the plotly canvas, so it sets font sizes and
    resolution. Falls back to default_cm if the row/columns are missing."""
    width_cm, height_cm = _read_cm(stem, "RenderWidth", "RenderHeight", default_cm)
    return round(width_cm * _CM_TO_PX), round(height_cm * _CM_TO_PX)


def chart_display_cm(stem, default_cm):
    """Display size (width_cm, height_cm) shown in the paper, from DisplayWidth/
    DisplayHeight (cm) in chartTable.csv. Applied via the DPI tag, not the canvas.
    Falls back to default_cm if the row/columns are missing."""
    return _read_cm(stem, "DisplayWidth", "DisplayHeight", default_cm)


def _png_with_dpi(png_bytes, dpi):
    """Insert a pHYs chunk so the PNG reports `dpi`. kaleido writes no pHYs, so we
    splice one in right after IHDR without re-encoding the image data."""
    ppm = int(round(dpi / _CM_PER_INCH * 100))  # pixels per metre (pHYs unit 1 = metre)
    body = b"pHYs" + struct.pack(">IIB", ppm, ppm, 1)
    chunk = struct.pack(">I", 9) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    ihdr_end = 8 + 4 + 4 + 13 + 4  # signature + IHDR (len + type + 13 data + crc)
    return png_bytes[:ihdr_end] + chunk + png_bytes[ihdr_end:]


def smart_save_image(fig, output_path, display_cm, scale=2):
    """Render `fig` and tag the PNG so a bare \\includegraphics shows it at
    display_cm = (width_cm, height_cm), aspect preserved (the image fits inside
    that box). Writes only when the bytes change (avoids needless churn)."""
    new_bytes = pio.to_image(fig, format="png", scale=scale)
    px_w = int.from_bytes(new_bytes[16:20], "big")   # IHDR width
    px_h = int.from_bytes(new_bytes[20:24], "big")   # IHDR height
    width_cm, height_cm = display_cm
    # DPI that fits the bitmap inside the display box without distortion.
    dpi = max(px_w / (width_cm / _CM_PER_INCH), px_h / (height_cm / _CM_PER_INCH))
    new_bytes = _png_with_dpi(new_bytes, dpi)
    if output_path.exists() and output_path.read_bytes() == new_bytes:
        print(f"  [SmartSave] Skipping {output_path.name} (no changes)")
        return False
    output_path.write_bytes(new_bytes)
    print(f"  [SmartSave] Updating {output_path.name}")
    return True


def write_pdf(fig, output_path, render_width_px, display_width_cm):
    """Write a vector PDF sized to the display width (cm), matching the PNG. The
    figure is laid out on the (high-resolution) render canvas; scaling the PDF
    page by display/render makes its natural size equal the display size, so a
    bare \\includegraphics{...pdf} renders it at the paper size. Assumes the
    display and render aspect ratios match (height follows from the scale)."""
    scale = display_width_cm * _CM_TO_PX / render_width_px
    fig.write_image(str(output_path), format="pdf", scale=scale)
