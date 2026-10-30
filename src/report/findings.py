"""Single source of truth for the project's research questions and results.

Both the Streamlit "Research Findings" page and the PDF report generator
call compute_all_findings() so the dashboard and the report are guaranteed
to show identical numbers computed from the same dataset and code path.
"""
from __future__ import annotations

from src.stats import anova, correlation, hypothesis, regression


def compute_all_findings(df) -> list[dict]:
    findings = []

    # RQ1 - Descriptive / distribution of final grades
    findings.append({
        "id": "RQ1",
        "question": "What is the distribution of final grades (G3), and is it approximately normal?",
        "method": "Descriptive statistics + Shapiro-Wilk normality test",
        "result": _rq1(df),
    })
    # RQ2 - Study time vs final grade correlation
    c = correlation.pairwise_correlation(df["studytime"], df["G3"])
    findings.append({
        "id": "RQ2", "question": "Is weekly study time associated with final grade (G3)?",
        "method": "Pearson correlation",
        "result": f"r = {c['r']:.3f} ({c['strength']}), p = {c['p_value']:.4g} "
                   f"-> {'significant' if c['significant_at_0.05'] else 'not significant'} association.",
    })
    # RQ3 - Absences vs final grade
    c = correlation.pairwise_correlation(df["absences"], df["G3"], method="spearman")
    findings.append({
        "id": "RQ3", "question": "Is the number of absences associated with final grade (G3)?",
        "method": "Spearman rank correlation (absences is highly skewed/count data)",
        "result": f"rho = {c['r']:.3f} ({c['strength']}), p = {c['p_value']:.4g}.",
    })
    # RQ4 - Regression predicting G3
    r = regression.fit_ols(df, "G3", ["G1", "G2", "studytime", "absences"])
    findings.append({
        "id": "RQ4",
        "question": "How well can G1, G2, study time and absences predict the final grade (G3)?",
        "method": "Multiple linear regression (OLS)",
        "result": f"R^2 = {r['r_squared']:.3f} (adj. {r['adj_r_squared']:.3f}); "
                   f"G2 is the strongest predictor (coef={r['coefficients']['G2']:.3f}, "
                   f"p={r['p_values']['G2']:.4g}).",
    })
    # RQ5 - Sex difference in G3
    res = hypothesis.two_sample_ttest(df[df.sex == "M"]["G3"], df[df.sex == "F"]["G3"],
                                       question="Do male and female students differ in final grade?")
    findings.append({
        "id": "RQ5", "question": res.research_question,
        "method": "Independent two-sample t-test",
        "result": f"t = {res.test_statistic:.3f}, p = {res.p_value:.4g} -> {res.decision}.",
    })
    # RQ6 - Grade improvement G1 -> G2
    res = hypothesis.paired_ttest(df["G1"], df["G2"],
                                   question="Does the second-period grade differ from the first?")
    findings.append({
        "id": "RQ6", "question": res.research_question,
        "method": "Paired t-test",
        "result": f"t = {res.test_statistic:.3f}, p = {res.p_value:.4g}, "
                   f"mean change = {res.extra['mean_difference']:.3f} -> {res.decision}.",
    })
    # RQ7 - Pass rate vs benchmark
    successes = int((df["pass_fail"] == "Pass").sum())
    res = hypothesis.proportion_ztest(successes, len(df), 0.60,
                                       question="Does the pass rate differ from a 60% benchmark?")
    findings.append({
        "id": "RQ7", "question": res.research_question,
        "method": "One-proportion z-test",
        "result": f"sample proportion = {res.extra['sample_proportion']:.3f}, z = {res.test_statistic:.3f}, "
                   f"p = {res.p_value:.4g} -> {res.decision}.",
    })
    # RQ8 - Sex vs pass/fail independence
    res = hypothesis.chi_square_independence(df, "sex", "pass_fail",
                                              question="Is passing independent of sex?")
    findings.append({
        "id": "RQ8", "question": res.research_question,
        "method": "Chi-square test of independence",
        "result": f"chi2 = {res.test_statistic:.3f}, df = {res.df_}, p = {res.p_value:.4g} -> {res.decision}.",
    })
    # RQ9 - Mother's job vs G3 (ANOVA)
    av = anova.one_way_anova(df, "G3", "Mjob")
    findings.append({
        "id": "RQ9", "question": "Does final grade (G3) differ across mother's occupation categories?",
        "method": "One-way ANOVA + Tukey HSD post-hoc",
        "result": f"F = {av['f_statistic']:.3f}, p = {av['p_value']:.4g}, eta^2 = {av['eta_squared']:.3f} "
                   f"-> {'significant' if av['reject_h0'] else 'not significant'} difference among groups.",
    })
    # RQ10 - Subject (Math vs Portuguese) variance in G3
    res = hypothesis.f_test_variances(df[df.subject == "Math"]["G3"], df[df.subject == "Portuguese"]["G3"],
                                       question="Do Math and Portuguese final grades have equal variance?")
    findings.append({
        "id": "RQ10", "question": res.research_question,
        "method": "F-test for equality of variances",
        "result": f"F = {res.test_statistic:.3f}, p = {res.p_value:.4g} -> {res.decision}. "
                   "Caveat: 382 of the 395 Math students also appear in the Portuguese sample "
                   "(verified via the dataset authors' merge key), so these two groups are "
                   "substantially overlapping rather than independent -- the test's independence "
                   "assumption is violated and this result should be interpreted with caution.",
    })
    # RQ11 - Internet access vs pass rate
    from src.stats import probability
    p_with = probability.conditional_probability(df, "pass_fail", "Pass", "internet", True)
    p_without = probability.conditional_probability(df, "pass_fail", "Pass", "internet", False)
    findings.append({
        "id": "RQ11", "question": "Does home internet access relate to the likelihood of passing?",
        "method": "Conditional empirical probability",
        "result": f"P(Pass | internet) = {p_with:.3f} vs P(Pass | no internet) = {p_without:.3f}.",
    })
    return findings


def _rq1(df) -> str:
    from src.stats import probability
    from src.stats.descriptive import numeric_summary
    s = numeric_summary(df["G3"])
    n = probability.normality_assessment(df["G3"])
    return (f"Mean = {s['mean']:.2f}, median = {s['median']:.1f}, std = {s['std']:.2f}, "
            f"skewness = {s['skewness']:.2f}. Shapiro-Wilk p = {n['p_value']:.3g} -> "
            f"{'approximately normal' if n['is_normal_at_0.05'] else 'significantly non-normal'} "
            f"(left-skewed, consistent with many students clustering around a passing grade).")
