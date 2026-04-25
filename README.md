# Bachelor Thesis Repository

Electrical characterization of organic field-effect transistors (OFETs) using a current-driven gated van der Pauw (vdP) method.

## Background

The soft material properties of organic semiconductors make them attractive
for future display technology. Think about foldable cell phones or large area screens that can
be rolled up. The development of such devices, however, requires an excellent understanding
of the physics of charge transport within these semiconductors. The goal of our research is
to advance this understanding with characterization techniques that cover transport distances
form the molecular level up to the macroscopic dimensions of entire devices.
Experiments on charge transport can be spoiled by many extrinsic effects, most often by
electronic contact resistances. One outstanding technique that circumvents these perils is
the Van der Pauw method. It allows measurements of the semiconductor’s conductivity and
provides a direct view onto the charge transport across the device.

## Overview

This repository contains measurement data, analysis notebooks, and simulation scripts developed during a bachelor thesis focused on O-FET electrical characterization.

The central idea is to combine classical transistor characterization (IDS-VGS, IDS-VDS, IGS-VGS) with a gated vdP geometry and current-driven protocols to evaluate transport behavior, contact effects, and sheet-related electrical properties under gate control.

## Thesis Scope

Main objectives covered by this repository:

- Extract transfer and output characteristics of O-FET devices.
- Compare multiple material/process variants (for example ALD, PaN, PS-cook, PS9, PS12).
- Analyze leakage currents and measurement consistency.
- Evaluate current-driven gated vdP measurements for lateral transport characterization.
- Support interpretation with numerical simulation of vdP potential distributions.

## Repository Structure

Top-level folders are organized by material/device batch and by simulation/testing tasks.

- `ALD1106/`: Device data and notebooks for ALD-related sample set.
- `PaN/`: Characterization notebooks and IDS-VGS data for PaN sample set.
- `PS-cook/`, `PS9/`, `PS12/`: Main O-FET analysis workspaces with transfer/output/gate-leakage and vdP-related measurements.
- `Simulation/`: Numerical vdP potential simulations (square/round/cloverleaf variants) and generated log files.
- `OFET Simulation/`: Additional MOSFET/O-FET conceptual simulation script.
- `Test/`: Early testing notebooks and helper scripts.
- `Literature/`: Reference material for the thesis background.

Typical measurement data subfolders:

- `Data-IDS-VGS/`: Transfer curves.
- `Data-IDS-VDS/`: Output curves.
- `Data-IGS-VGS/`: Gate leakage curves.
- `Data-vdP/`: van der Pauw current/voltage data.

## Data and Naming

- Most raw data files are text-based (`.txt`, in some scripts also `.dat`).
- File names commonly use timestamp-like numeric IDs (for example `20262204001.txt`).
- Plot scripts/notebooks generally assume fixed folder names and relative paths.

If you add new measurements, keep the folder naming pattern and relative path structure to avoid breaking notebook/script imports.

## Analysis Workflow

The standard workflow in this repository is:

1. Acquire raw measurement files from instrument software.
2. Place files into the corresponding `Data-*` directory for a given sample set.
3. Run characterization notebooks:
	- `characterization.ipynb`
	- `mobility.ipynb`
	- `resistance.ipynb`
	- `resistance-vdP.ipynb` (where available)
4. Export publication-ready figures and compare across sample families.
5. Use `Simulation/` scripts to interpret geometry- and contact-dependent vdP behavior.

## Simulations

The `Simulation/` directory contains finite-difference style potential-relaxation scripts for vdP structures (for example `vdP-round.py`, `vdP-square.py`, and cloverleaf variants).

These scripts:

- Solve potential distributions on a 2D grid.
- Apply boundary/contact constraints for current injection and voltage sensing.
- Report corner potentials and potential fractions.
- Export figures (`.png`, `.eps`) and text logs (`vdP_log_*.txt`).

## Reproducibility Notes

- Keep raw files unchanged; perform processing in notebooks/scripts only.
- Preserve original measurement IDs in generated plots and tables.
- Record simulation parameters (`n`, `n_iter`, contact size, bias conventions) in exported logs.
- When comparing batches, use consistent axis limits and unit scaling.

## Current Status

This repository is an active research workspace for thesis development, containing:

- Raw and curated measurement data.
- Iterative analysis notebooks.
- Figure generation scripts.
- Numerical support simulations.

As the thesis progresses, notebook outputs and folder contents may continue to evolve.

## Author

Bachelor thesis project on O-FET electrical characterization via current-driven gated van der Pauw methodology.

## Supervisor

Prof. Dr. R. Kersting, roland.kersting@lmu.de, Nano-Institut der Ludwig-Maximilians-Universität München, Germany.
