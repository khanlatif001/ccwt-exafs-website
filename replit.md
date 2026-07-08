# CCWT-EXAFS Website

## Overview
A Flask web app for Continuous Cauchy Wavelet Transform (CCWT) analysis of EXAFS
(Extended X-ray Absorption Fine Structure) spectra. Users upload a two-column
`k, chi(k)` data file and get back interactive Plotly plots: the interpolated
EXAFS signal, its Fourier transform, and the CCWT heatmap (k vs. R) with
colorscale and contrast controls, matching the original analysis script by
Latif Ullah Khan (SESAME BM08-XAFS/XRF beamline), based on Munoz, Argoul &
Farges (2003), American Mineralogist 88, 694-700.

## Structure
- `app.py` — Flask routes: `/` (upload form) and `/analyze` (runs the
  transform and renders results).
- `ccwt.py` — Pure computation module ported from the original standalone
  script (`compute_ccwt`), independent of Flask so it can be tested/reused.
- `templates/` — Jinja2 templates (`base.html`, `index.html`, `results.html`).
- `static/style.css` — Site styling.
- `sample_data/k2_sample.dat` — Synthetic sample data for smoke-testing the
  upload flow (not real experimental data).

## Running
The `Start application` workflow runs `python app.py`, serving on port 5000
(Flask debug mode). No secrets or external services are required; uploaded
files are processed in memory and not persisted to disk.

## Notes
- Accepted upload extensions: `.dat`, `.txt`, `.csv`, `.xafs`. Max file size 5 MB.
- Advanced parameters (Cauchy order `n`, R-range, k-range) are optional; the
  original script's defaults are used if left blank.
- `SESSION_SECRET` env var is used for Flask's session secret if present.
