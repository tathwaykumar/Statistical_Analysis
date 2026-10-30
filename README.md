# Statistical Data Analysis and Insights Platform

A Comprehensive Statistical Investigation Using Probability, Correlation, Regression, Hypothesis
Testing, ANOVA and Interactive Visualization — built on the real-world UCI Student Performance
dataset.

**Student:** Tathwa Y Kumar · B.Tech CSE (Data Science) · VIT Vellore
**Course:** Probability and Statistics · Fall Semester 2026

This is an independent additional-learning project. It has not been submitted for, or claimed to
receive, any academic credit, approval or endorsement.

## Overview
The platform ingests, cleans and analyzes a real, publicly sourced educational dataset
(UCI "Student Performance," Cortez & Silva 2008; 1,044 real student records) and exposes the full
analysis through an interactive Streamlit dashboard plus a generated academic PDF report. Every
number shown anywhere in the project — dashboard or PDF — is computed live from the dataset by a
shared statistics engine; nothing is hardcoded.

## Objectives
- Apply descriptive statistics, probability, correlation, regression, hypothesis testing and
  ANOVA to a genuine dataset.
- Independently verify every nontrivial calculation (see `tests/`).
- Communicate findings through a premium, interactive dashboard and a reproducible PDF report.

## Features
- 13-page interactive Streamlit dashboard (Executive Overview, Dataset Explorer, Data Quality,
  Descriptive Statistics, Probability & Distributions, Correlation, Regression, Hypothesis
  Testing, ANOVA, Interactive Visualizations, Research Findings, Report Generation, About).
- Adjustable significance level (0.01 / 0.05 / 0.10) propagated live to every test.
- CSV export of filtered/cleaned data; one-click PDF report generation and download.
- Mandatory ANOVA sum-of-squares validation (SST = SSB + SSW) shown on-screen.
- 22 automated tests cross-checking statistical calculations against SciPy/manual ground truth.

## Technology stack
Python · Pandas · NumPy · SciPy · Statsmodels · scikit-learn · Streamlit · Plotly · Matplotlib ·
ReportLab · Pytest.

## Installation
```bash
pip install -r requirements.txt
```

## Running the dashboard
```bash
streamlit run app/Home.py
```

## Generating the PDF report (CLI)
```bash
python -m src.report.pdf_report
```
Output: `outputs/reports/Statistical_Data_Analysis_Report.pdf`

## Running tests
```bash
pytest tests/ -v
```

## Dataset
UCI Machine Learning Repository — "Student Performance" (Cortez & Silva, 2008). Raw files
preserved untouched in `data/raw/`. Full source/license/data-dictionary: `docs/DATASET_SOURCE.md`.

## Folder structure
```
config/                        student_config.py (identity), private.env (gitignored secrets)
data/raw/                      original UCI CSVs, untouched
data/processed/                cleaned dataset output
src/data/                      ingestion & cleaning
src/stats/                     descriptive, probability, correlation, regression, hypothesis, anova
src/visualization/             Plotly chart builders for the dashboard
src/report/                    findings (shared by dashboard+PDF), chart PNGs, PDF generator
app/                           Streamlit multipage dashboard
tests/                         pytest suite, cross-checked against SciPy/manual calculations
docs/                          PROJECT_REPORT, METHODOLOGY, DATASET_SOURCE, STATISTICAL_METHODS, USER_GUIDE
outputs/reports/               generated academic PDF report
screenshots/                   dashboard screenshots (light/dark mode, before/after audit fixes)
screenshots/presentation_assets/  cropped screenshots embedded in the slide deck
Statistical_Analysis_Presentation.pptx  slide deck (project root, standalone file)
```

## Testing instructions
See "Running tests" above. All 24 tests must pass; CI is not configured (local project).

## Screenshots
See the `screenshots/` folder for dashboard screenshots captured during development and the
Playwright visual audit (light mode, simulated dark mode, before/after fixes). Or run the
dashboard locally (see above) to view it live.

## Presentation
`Statistical_Analysis_Presentation.pptx` (project root) is a 23-slide academic deck covering the
full research narrative — dataset, methodology, descriptive statistics, probability, correlation,
regression, hypothesis testing and ANOVA — built from the same verified numbers as the dashboard
and PDF report.

## Documentation
- `docs/PROJECT_REPORT.md` — markdown companion to the PDF report
- `docs/METHODOLOGY.md` — research design and data/statistical methodology
- `docs/DATASET_SOURCE.md` — dataset provenance, license, full data dictionary
- `docs/STATISTICAL_METHODS.md` — assumptions and verification per method
- `docs/USER_GUIDE.md` — how to use the dashboard
- `docs/VIVA_QA.md` — anticipated viva questions and answers
- `docs/DEMONSTRATION_GUIDE.md` — suggested walkthrough order for a live demo
