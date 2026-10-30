# Progress Checklist

- [x] Phase 1 — Research & Foundation: dataset researched (5 candidates), UCI Student Performance
  selected, downloaded, raw files preserved, data dictionary written, 11 research questions
  defined, architecture scaffolded.
- [x] Phase 2 — Data Engineering: ingestion (`src/data/ingest.py`), cleaning with full audit log
  (`src/data/clean.py`), no silent row drops, tests passing.
- [x] Phase 3 — Statistical Engine: descriptive, probability, correlation, regression, hypothesis
  testing, ANOVA modules implemented and validated (SST=SSB+SSW, F cross-check, R² cross-check).
- [x] Phase 4 — Dashboard: 13-page Streamlit app built, premium styling, all pages verified with
  `streamlit.testing.v1.AppTest` (headless, zero exceptions) and interactivity confirmed
  (dropdown change -> recalculated result).
- [x] Phase 5 — Research Documentation: findings module shared by dashboard + PDF, PDF report
  generator (ReportLab) producing a 12-page report with cover page, all required sections, charts
  and tables, consistent with dashboard numbers.
- [x] Phase 6 — Quality Assurance: 22 automated tests passing (`pytest tests/ -v`), dashboard
  smoke-tested end to end, PDF generation verified (page count, file size), one real bug found and
  fixed during testing (a `st.write` magic-detection issue on `7_Hypothesis_Testing.py`).
- [x] Phase 7 — Final Delivery: application, raw + processed data, statistics modules, dashboard,
  PDF report, source code, docs (README, PROJECT_REPORT, METHODOLOGY, DATASET_SOURCE,
  STATISTICAL_METHODS, USER_GUIDE, VIVA_QA, DEMONSTRATION_GUIDE), automated tests, this checklist.

## Known follow-ups (not blockers)
- Two-way ANOVA (`anova.two_way_anova`) is implemented but not yet given its own dashboard page.
- No git repository initialized yet in this directory (git init + first commit is a user decision,
  not made automatically per the Git Safety Protocol).

- [x] Phase 8 — Statistical/Academic Audit: independent re-verification of every calculation
  (regression, t-tests, chi-square, ANOVA incl. SST=SSB+SSW) against raw SciPy/Statsmodels and
  manual formulas; discovered and fixed an understated dataset-merge overlap (382 of 395 Math
  students also appear in the Portuguese file, verified via the dataset authors' own
  student-merge.R key — 1,044 rows represent only ~662 unique students). Fix disclosed consistently
  in Data Quality page, Hypothesis Testing F-test page, DATASET_SOURCE.md, and the PDF report.
  See `docs/FINAL_AUDIT_REPORT.md`.
- [x] Phase 9 — Visual/UX Audit (Playwright MCP): installed and connected the official Playwright
  MCP server (`.mcp.json`, project-scoped); visited all 13 pages, inspected charts/legends/tables
  under both light and simulated-dark OS colour schemes. Root cause of "white on white" legends:
  `st.plotly_chart()` auto-recolours figures to match the viewer's ambient browser/OS theme unless
  `theme=None` is passed, and no `.streamlit/config.toml` pinned a theme, so a dark-mode browser
  silently overrode the app's explicit navy/white colour system. Fixed by pinning a light theme in
  `.streamlit/config.toml`, adding `theme=None` to all 15 `st.plotly_chart()` calls, and giving
  the previously-unstyled raw charts on the Interactive Visualizations page the same consistent
  template (`src/visualization/plots.py::style_figure`). Also found and fixed two real functional
  bugs while testing: a bare ternary expression on the ANOVA page that leaked raw
  `DeltaGenerator`/Python-object debug text onto the screen (same bug class as an earlier fix on
  Hypothesis Testing), and a regression-coefficients table rendering an extremely small p-value
  (~1.87e-166) as ~170 literal zeros instead of scientific notation. Re-verified all 13 pages and
  the PDF after fixes; full pytest suite re-run (24/24 passing). See `docs/FINAL_AUDIT_REPORT.md`.
