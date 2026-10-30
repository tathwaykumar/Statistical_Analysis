# Demonstration Guide

Suggested 8-10 minute walkthrough order for showing this project live.

1. **Home** — point out live headline stats (observations, variables, missing %) and the three
   key-finding cards (correlation, regression R², ANOVA F) computed live, not static text.
2. **Dataset Explorer** — filter by subject/sex/school to show the data is real and filterable;
   download a filtered CSV.
3. **Data Quality & Cleaning** — show the cleaning log and explain the "flag, don't delete"
   outlier policy.
4. **Descriptive Statistics** — switch the variable dropdown (e.g. G3 -> absences) to show
   histogram/box/density plots update immediately.
5. **Probability & Distributions** — show the Bayes' theorem worked example and the Shapiro-Wilk
   normality verdict on G3 (non-normal, left-skewed — explain why).
6. **Correlation Analysis** — switch between Pearson/Spearman, point out the heatmap and the
   explicit "correlation is not causation" note.
7. **Regression Analysis** — change predictors live, show R²/coefficients update, point out the
   VIF multicollinearity check and residual diagnostics.
8. **Hypothesis Testing** — switch between the 7 available tests in the dropdown; show the full
   H0/H1/statistic/decision block for at least two tests (e.g. sex t-test, chi-square).
9. **ANOVA** — this is the centerpiece: show the SST = SSB + SSW validation banner going green,
   change the significance level in the sidebar and show the decision updating live.
10. **Report Generation** — click "Generate PDF report," open the resulting PDF, and show a
    number (e.g. the regression R²) matches what was just seen on screen.
11. **Research Findings / About** — close by scrolling the 11 research questions and mentioning
    the integrity commitments (no fabricated data, no hardcoded results, automated tests).

If asked to prove nothing is hardcoded: open `src/report/findings.py` and show it calls into
`src/stats/*` directly on the DataFrame, then run `pytest tests/ -v` live to show the automated
cross-checks passing.
