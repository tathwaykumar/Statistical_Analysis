# User Guide

## Starting the application
```
pip install -r requirements.txt
streamlit run app/Home.py
```
Open the URL Streamlit prints (default http://localhost:8501).

## Navigating
Use the page list in the left sidebar. Pages, in order:
1. **Home (Executive Overview)** — headline stats and key findings at a glance.
2. **Dataset Explorer** — filter by subject/sex/school, browse and export rows.
3. **Data Quality & Cleaning** — see exactly what cleaning was done and why.
4. **Descriptive Statistics** — pick any numeric or categorical variable for full summary stats and charts.
5. **Probability & Distributions** — empirical/conditional probability, Bayes' theorem, normality testing.
6. **Correlation Analysis** — correlation matrix, pairwise test with significance, scatter + trendline.
7. **Regression Analysis** — pick target/predictors, see coefficients, diagnostics, train/test metrics.
8. **Hypothesis Testing** — pick a test from the dropdown; full H0/H1/statistic/p-value/decision shown.
9. **ANOVA** — pick a dependent variable and grouping factor; SST=SSB+SSW validation shown live.
10. **Interactive Visualizations** — build your own scatter/box/violin/bar/pair plots.
11. **Research Findings** — the 11 research questions with live-computed answers.
12. **Report Generation** — regenerate and download the full academic PDF report; export CSV/log.
13. **About the Project** — identity, dataset and integrity summary.

## Changing the significance level
Use the "Significance level (alpha)" control in the sidebar on the Hypothesis Testing / ANOVA
pages. All tests and decisions on that page recompute immediately using the new alpha.

## Generating the PDF report
Go to **Report Generation** → click "Generate PDF report" → use the download button that appears.
The report is also written to `outputs/reports/Statistical_Data_Analysis_Report.pdf` and can be
regenerated from the command line at any time:
```
python -m src.report.pdf_report
```

## Running the tests
```
pytest tests/ -v
```

## Where things live
- Raw data: `data/raw/`
- Cleaned data: `data/processed/` (also downloadable from the dashboard)
- Statistical engine: `src/stats/`
- Dashboard pages: `app/pages/`
- Report generator: `src/report/`
- Student/project identity config: `config/student_config.py` (reads `config/private.env`,
  which is gitignored — edit that file to set your own registration number/faculty name).
