# Statistical Methods Reference

For each method: what it does, key assumptions, and how it is independently verified in this
project.

## Descriptive statistics
- **Assumptions:** none (purely descriptive).
- **Verification:** `tests/test_descriptive.py` checks computed mean/median/std/variance/range
  against manual NumPy/Pandas calculations and a known textbook example.

## Probability & distributions
- **Empirical/conditional/joint probability:** relative frequency estimators; valid as long as
  the sample is representative of the population of interest (a limitation, not a guarantee,
  here — see `docs/PROJECT_REPORT.md` limitations).
- **Shapiro-Wilk normality test:** H0 = data drawn from a normal distribution. Assumption: sample
  size reasonably large but not so large the test becomes over-sensitive to trivial deviations
  (capped at n=5000 here via sampling).

## Correlation (Pearson / Spearman)
- **Pearson assumptions:** linear relationship, continuous variables, bivariate normality (for
  exact inference; large-sample CLT gives practical robustness).
- **Spearman:** rank-based, no distributional assumption, robust to monotonic non-linearity and
  outliers — used for skewed count variables such as `absences`.
- **Verification:** `tests/test_correlation.py` checks `r` and `p` against `scipy.stats.pearsonr`
  directly, and checks the 95% CI contains the point estimate.

## Regression (OLS)
- **Assumptions checked:** linearity (scatter/trendline), independence (design), homoscedasticity
  (residuals-vs-fitted correlation proxy), residual normality (Shapiro-Wilk on residuals),
  multicollinearity (VIF; VIF > 5 flagged).
- **Verification:** `tests/test_regression.py` recovers a known synthetic linear relationship
  (intercept, slope) and independently recomputes R² from residual/total sum of squares.

## Hypothesis testing
- Every test returns a `TestResult` with H0, H1, alpha, assumptions, statistic, df, p-value,
  critical value and (where applicable) a confidence interval — the full reporting checklist
  required by the project brief.
- Two-sample t-test automatically runs Levene's test to decide Welch vs. pooled-variance t-test.
- **Verification:** `tests/test_hypothesis.py` checks t-statistics, p-values and chi-square
  statistics against SciPy's own implementations on hand-built examples with known outcomes.

## ANOVA
- **Mandatory validation:** SST = SSB + SSW is recomputed independently of
  `scipy.stats.f_oneway` from raw group means, and both the sum-of-squares identity and the
  F-statistic are cross-checked against `f_oneway`'s output (`decomposition_valid`,
  `f_cross_check_valid`).
- **Assumptions checked:** independence (design), homogeneity of variance (Levene's test).
  When Levene's test fails at the chosen alpha, Welch/Alexander-Govern ANOVA is reported as a
  robust alternative.
- **Post-hoc:** Tukey HSD run automatically when the omnibus test is significant and there are
  more than two groups.
- **Verification:** `tests/test_anova.py` checks the SST=SSB+SSW identity, matches
  `scipy.stats.f_oneway`, and checks degrees of freedom on hand-built groups.

## Correlation vs. causation
Explicitly called out next to every correlation and regression result in the dashboard and PDF
report: association does not imply causation, and no causal claims are made anywhere in this
project.
