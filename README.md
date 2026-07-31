# Productive Spending Policy Experiments

This repository reproduces **Long-Term Gains in Output**, a six-panel
summary of productive public-spending policy experiments for advanced economies
and emerging market and developing economies.

The retained experiments cover:

- permanent reallocations of 1 percent of GDP from public consumption toward
  infrastructure, human capital, or R&D;
- gradual closure of infrastructure, human-capital, and R&D spending-efficiency
  gaps;
- EMDE efficiency reforms at two closure speeds, completing the gap narrowing by
  2050 or, faster, by 2040; and, at each speed, a sensitivity case whose initial
  gaps are exactly 10 percentage points above the calibrated gaps and are
  narrowed by the same amount;
- a 50/50 human-capital and R&D spending mix; and
- faster and slower private-sector technology diffusion.

The compiled result is [`results/summary.pdf`](results/summary.pdf). No other
model experiments or analytical documents are included.

## Structure

```text
drivers/          Reduced MATLAB simulation and export drivers
models/           Shared Dynare model source and 21 retained result files
scripts/          Five Python chart generators for the six panels
data/             Annual output responses used by the charts
results/          Figure 13 source, PDF, and panel outputs
```

## Requirements

- MATLAB R2024b
- Dynare 5.5
- IRIS Toolbox
- Python 3.11 or later
- A LaTeX distribution with `latexmk` and `pdflatex`

Install the Python packages with:

```bash
python3 -m pip install -r requirements.txt
```

The default MATLAB paths match the local installation used to generate the
committed results. Set these environment variables when the toolboxes are
installed elsewhere:

```bash
export IRIS_PATH=/path/to/iris
export DYNARE_PATH=/path/to/dynare/matlab
```

## Reproduce Figure 13

To rebuild the dataset, charts, and results document from the committed model
outputs:

```bash
invoke rebuild
```

To solve all 21 experiments before rebuilding the figure:

```bash
invoke all
```

The stages can also be run separately:

```bash
invoke models
invoke export
invoke charts
invoke document
```

`MODEL_FILTER` can restrict a model run to names containing a substring. For
example, this runs only the higher-gap variants:

```bash
MODEL_FILTER=low invoke models
```
