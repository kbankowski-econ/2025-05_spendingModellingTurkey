"""Reproducibility tasks for Figure 13."""

from pathlib import Path
import sys

from invoke import task


ROOT = Path(__file__).resolve().parent
MATLAB = "/Applications/MATLAB_R2024b.app/bin/matlab"
PLOT_SCRIPTS = [
    "plotReallocationAE.py",
    "plotReallocationEM.py",
    "plotPolicyEfficiency.py",
    "plotHumanCapitalIRFs.py",
    "plotDiffusionAE.py",
]


@task(name="models")
def solve_models(c):
    """Solve the 21 policy experiments and canonicalize their MAT files."""
    command = (
        f'{MATLAB} -batch "cd(\'{ROOT}\'); iniProject; '
        "run('drivers/runModel.m')\""
    )
    c.run(command, warn=True)


@task
def export(c):
    """Export annual output responses for the retained experiments."""
    command = (
        f'{MATLAB} -batch "cd(\'{ROOT}\'); iniProject; '
        "run('drivers/runSimulExport.m')\""
    )
    c.run(command)


@task
def charts(c):
    """Generate the six Figure 13 panels."""
    for script in PLOT_SCRIPTS:
        c.run(f'"{sys.executable}" "{ROOT / "scripts" / script}"')


@task
def document(c):
    """Compile the one-page Figure 13 results document."""
    c.run(
        "SOURCE_DATE_EPOCH=946684800 "
        f'latexmk -g -pdf -cd "{ROOT / "results" / "summary.tex"}"'
    )


@task(pre=[export, charts, document])
def rebuild(c):
    """Rebuild Figure 13 from the committed model results."""
    print("Figure 13 rebuilt from committed simulation results.")


@task(pre=[solve_models, export, charts, document])
def all(c):
    """Rerun every retained experiment and rebuild Figure 13."""
    print("All policy experiments and Figure 13 rebuilt.")
