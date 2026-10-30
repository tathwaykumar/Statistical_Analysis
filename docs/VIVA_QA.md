# Viva Questions and Answers

**Q1. Why did you choose the UCI Student Performance dataset over other options?**
It had zero missing values, an official data dictionary, a good mix of 15 numeric and 17
categorical variables, and genuinely supported every required technique (correlation, regression,
hypothesis testing, ANOVA) without forcing anything. I evaluated five candidates against explicit
criteria before choosing it — see `docs/DATASET_SOURCE.md`.

**Q2. How do you know your ANOVA results are correct, not just copied from a library?**
I independently recompute SSB, SSW and SST from the raw group means and verify
SST = SSB + SSW numerically (`decomposition_valid` in `src/stats/anova.py`), and cross-check my
manually recomputed F-statistic against `scipy.stats.f_oneway`'s output
(`f_cross_check_valid`). Both checks are unit-tested in `tests/test_anova.py` and shown live on
the ANOVA dashboard page.

**Q3. What's the difference between statistical and practical significance here?**
The ANOVA on mother's job vs. final grade is statistically significant (p < 0.001) but the effect
size (eta² ≈ 0.03) is small — mother's job explains only about 3% of grade variance. So it's
statistically real but not a practically large driver of outcomes.

**Q4. Why use both Pearson and Spearman correlation?**
Pearson assumes a linear relationship and is sensitive to outliers; Spearman is rank-based and
robust to skew/non-linearity. `absences` is heavily right-skewed (many zeros, a few large values),
so Spearman is the more appropriate choice there, while grade variables are closer to linear.

**Q5. How do you handle the assumption of equal variances in your t-tests?**
`two_sample_ttest` runs Levene's test first; if variances are judged unequal (p ≤ 0.05) it
automatically switches to Welch's t-test (unequal-variance) instead of the pooled-variance
version, and reports which was used.

**Q6. Does your regression model prove that studying more causes better grades?**
No — regression and correlation here show association, not causation. I say this explicitly next
to every regression/correlation result in both the dashboard and the PDF report. There could be
confounders (e.g. motivated students both study more and perform better for other reasons).

**Q7. How did you verify your calculations are not hardcoded?**
Both the dashboard's "Research Findings" page and the PDF report call the same function,
`compute_all_findings()` in `src/report/findings.py`, which itself calls the live statistics
modules on the current dataset. `tests/test_report_consistency.py` checks this function returns
identical results on repeated calls (reproducibility) and that the PDF builds without error.

**Q8. What would you do differently with more time/data?**
Collect a persistent student ID across both subject files (the current dataset only lets you
probabilistically match 382 overlapping students via identical attributes, which I chose not to
rely on), and extend to a two-way ANOVA with interaction terms (already implemented in
`src/stats/anova.py::two_way_anova` but not yet surfaced on a dedicated dashboard page).

**Q9. Why did you flag outliers instead of removing them?**
Because they are legitimate extreme observations (e.g. a student with many absences), not data
entry errors. Removing them would artificially tighten variance estimates and bias downstream
hypothesis tests. This decision, and its rationale, is logged explicitly in the Data Quality page.

**Q10. How is the significance level configurable, and does the whole app respect it?**
A sidebar control on the Hypothesis Testing and ANOVA pages sets `st.session_state["alpha"]`
(default 0.05), which every test/ANOVA computation on those pages reads and recomputes against
immediately — confirmed with a Streamlit `AppTest` interactivity check during development.
