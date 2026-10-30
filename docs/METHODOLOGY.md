# Methodology

## Research design
This project follows a quantitative, secondary-data research design: a real, publicly available
dataset is analyzed using descriptive and inferential statistics to answer predefined research
questions. No experimental manipulation or data collection was performed by the author; the
contribution is in analysis design, implementation, verification and communication of results.

## Data collection methodology
Data collection was performed by the original dataset authors (Cortez & Silva, 2008) via school
reports and student-answered questionnaires at two Portuguese secondary schools. This project
performs no additional collection; it re-uses the public release in full (see
`docs/DATASET_SOURCE.md`).

## Data preprocessing methodology
1. Load both raw CSV files independently, tag with a `subject` column, concatenate.
2. Validate types: coerce all documented numeric columns to numeric dtype.
3. Check for missing values (`isna().sum()`) — none found, consistent with dataset documentation.
4. Check for exact full-row duplicates — remove only if found, logged.
5. Flag (not remove) IQR-rule outliers in numeric columns for transparency.
6. Convert yes/no columns to boolean.
7. Derive `average_grade`, `grade_trend`, `pass_fail` for convenience in later analysis.

All decisions and their outcomes are recorded in a `CleaningReport` object (see
`src/data/clean.py`) and surfaced verbatim in the "Data Quality & Cleaning" dashboard page and the
PDF report.

## Statistical methodology
Each module (`src/stats/*.py`) implements one family of techniques:

- **Descriptive statistics** (`descriptive.py`): mean, median, mode, range, variance, std,
  quartiles, IQR, skewness, kurtosis — computed with NumPy/Pandas/SciPy, not hand-rolled formulas,
  to avoid implementation error.
- **Probability** (`probability.py`): empirical/conditional/joint probability from observed
  frequencies, Bayes' theorem, Shapiro-Wilk normality testing, normal distribution fitting.
- **Correlation** (`correlation.py`): Pearson and Spearman coefficients with p-values (SciPy) and
  Fisher-z confidence intervals for Pearson r.
- **Regression** (`regression.py`): OLS via Statsmodels (gives p-values, R², F-statistic natively),
  VIF via Statsmodels' `variance_inflation_factor`, train/test split evaluation via scikit-learn.
- **Hypothesis testing** (`hypothesis.py`): one/two-sample and paired t-tests, proportion z-test,
  chi-square tests, F-test — each wrapped in a `TestResult` dataclass that forces every required
  reporting element (H0, H1, alpha, assumptions, statistic, df, critical value, p-value, CI,
  decision) to be present.
- **ANOVA** (`anova.py`): one-way ANOVA computed two ways — via `scipy.stats.f_oneway` and via an
  independent manual sum-of-squares decomposition — and cross-checked against each other
  (`decomposition_valid`, `f_cross_check_valid`). Welch's ANOVA is used automatically as a
  fallback path when Levene's test indicates unequal variances.

## Significance level
Default alpha = 0.05, adjustable in the dashboard sidebar (0.01 / 0.05 / 0.10) and propagated to
every hypothesis test and ANOVA on that page.

## Verification strategy
See `docs/STATISTICAL_METHODS.md` and `tests/` for the specific cross-checks used for each method
family (e.g. SST = SSB + SSW, R² from residuals, correlation against `scipy.stats.pearsonr`).
