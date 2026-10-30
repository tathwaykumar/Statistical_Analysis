"""Module E: hypothesis testing with full reporting of every required element."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats as sps


@dataclass
class TestResult:
    research_question: str
    h0: str
    h1: str
    alpha: float
    assumptions: list[str]
    test_statistic: float
    df_: float | tuple | None
    p_value: float
    critical_value: float | None = None
    ci: tuple | None = None
    extra: dict = field(default_factory=dict)

    @property
    def reject_h0(self) -> bool:
        return self.p_value < self.alpha

    @property
    def decision(self) -> str:
        return "Reject H0" if self.reject_h0 else "Fail to reject H0"

    def summary(self) -> dict:
        return {
            "research_question": self.research_question,
            "h0": self.h0,
            "h1": self.h1,
            "alpha": self.alpha,
            "assumptions": self.assumptions,
            "test_statistic": self.test_statistic,
            "degrees_of_freedom": self.df_,
            "p_value": self.p_value,
            "critical_value": self.critical_value,
            "confidence_interval": self.ci,
            "decision": self.decision,
            "extra": self.extra,
        }


def one_sample_ttest(sample: pd.Series, popmean: float, alpha: float = 0.05,
                      question: str = "") -> TestResult:
    s = sample.dropna().astype(float)
    stat, p = sps.ttest_1samp(s, popmean)
    n = len(s)
    se = s.std(ddof=1) / np.sqrt(n)
    tcrit = sps.t.ppf(1 - alpha / 2, n - 1)
    ci = (float(s.mean() - tcrit * se), float(s.mean() + tcrit * se))
    return TestResult(
        research_question=question or f"Does the sample mean differ from {popmean}?",
        h0=f"mu = {popmean}", h1=f"mu != {popmean}", alpha=alpha,
        assumptions=["Observations independent", "Approximately normal or n large enough (CLT)"],
        test_statistic=float(stat), df_=n - 1, p_value=float(p),
        critical_value=float(tcrit), ci=ci, extra={"sample_mean": float(s.mean()), "n": n},
    )


def two_sample_ttest(a: pd.Series, b: pd.Series, alpha: float = 0.05,
                      equal_var: bool | None = None, question: str = "") -> TestResult:
    a, b = a.dropna().astype(float), b.dropna().astype(float)
    if equal_var is None:
        _, lev_p = sps.levene(a, b)
        equal_var = lev_p > 0.05
    stat, p = sps.ttest_ind(a, b, equal_var=equal_var)
    df_ = len(a) + len(b) - 2 if equal_var else _welch_df(a, b)
    diff = float(a.mean() - b.mean())
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    tcrit = sps.t.ppf(1 - alpha / 2, df_)
    ci = (diff - tcrit * se, diff + tcrit * se)
    return TestResult(
        research_question=question or "Do the two group means differ?",
        h0="mu_a = mu_b", h1="mu_a != mu_b", alpha=alpha,
        assumptions=[
            "Independent samples",
            f"Variance equality assumed: {equal_var} (Levene test)",
            "Approximately normal within groups or n large enough",
        ],
        test_statistic=float(stat), df_=float(df_), p_value=float(p),
        critical_value=float(tcrit), ci=(float(ci[0]), float(ci[1])),
        extra={"mean_a": float(a.mean()), "mean_b": float(b.mean()), "equal_var_used": equal_var},
    )


def _welch_df(a: pd.Series, b: pd.Series) -> float:
    va, vb, na, nb = a.var(ddof=1), b.var(ddof=1), len(a), len(b)
    num = (va / na + vb / nb) ** 2
    den = (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    return float(num / den)


def paired_ttest(before: pd.Series, after: pd.Series, alpha: float = 0.05,
                  question: str = "") -> TestResult:
    diff = (after - before).dropna().astype(float)
    stat, p = sps.ttest_rel(after.dropna(), before.dropna())
    n = len(diff)
    se = diff.std(ddof=1) / np.sqrt(n)
    tcrit = sps.t.ppf(1 - alpha / 2, n - 1)
    ci = (float(diff.mean() - tcrit * se), float(diff.mean() + tcrit * se))
    return TestResult(
        research_question=question or "Does the paired measurement change significantly?",
        h0="mean difference = 0", h1="mean difference != 0", alpha=alpha,
        assumptions=["Paired observations", "Differences approximately normal"],
        test_statistic=float(stat), df_=n - 1, p_value=float(p),
        critical_value=float(tcrit), ci=ci, extra={"mean_difference": float(diff.mean())},
    )


def proportion_ztest(successes: int, n: int, p0: float, alpha: float = 0.05,
                      question: str = "") -> TestResult:
    phat = successes / n
    se0 = np.sqrt(p0 * (1 - p0) / n)
    z = (phat - p0) / se0
    p = 2 * (1 - sps.norm.cdf(abs(z)))
    se_hat = np.sqrt(phat * (1 - phat) / n)
    zcrit = sps.norm.ppf(1 - alpha / 2)
    ci = (phat - zcrit * se_hat, phat + zcrit * se_hat)
    return TestResult(
        research_question=question or f"Does the sample proportion differ from {p0}?",
        h0=f"p = {p0}", h1=f"p != {p0}", alpha=alpha,
        assumptions=["n*p0 >= 5 and n*(1-p0) >= 5 (normal approximation)"],
        test_statistic=float(z), df_=None, p_value=float(p),
        critical_value=float(zcrit), ci=(float(ci[0]), float(ci[1])),
        extra={"sample_proportion": float(phat)},
    )


def chi_square_independence(df: pd.DataFrame, col_a: str, col_b: str,
                             alpha: float = 0.05, question: str = "") -> TestResult:
    table = pd.crosstab(df[col_a], df[col_b])
    stat, p, dof, expected = sps.chi2_contingency(table)
    crit = sps.chi2.ppf(1 - alpha, dof)
    return TestResult(
        research_question=question or f"Are {col_a} and {col_b} independent?",
        h0=f"{col_a} and {col_b} are independent", h1=f"{col_a} and {col_b} are associated",
        alpha=alpha, assumptions=["Expected cell counts >= 5 recommended", "Independent observations"],
        test_statistic=float(stat), df_=int(dof), p_value=float(p), critical_value=float(crit),
        extra={"min_expected_count": float(expected.min()), "contingency_table": table.to_dict()},
    )


def chi_square_goodness_of_fit(observed: np.ndarray, expected: np.ndarray | None = None,
                                alpha: float = 0.05, question: str = "") -> TestResult:
    stat, p = sps.chisquare(observed, f_exp=expected)
    dof = len(observed) - 1
    crit = sps.chi2.ppf(1 - alpha, dof)
    return TestResult(
        research_question=question or "Does the observed distribution match the expected one?",
        h0="Observed frequencies match expected distribution",
        h1="Observed frequencies differ from expected distribution",
        alpha=alpha, assumptions=["Expected cell counts >= 5 recommended"],
        test_statistic=float(stat), df_=dof, p_value=float(p), critical_value=float(crit),
    )


def f_test_variances(a: pd.Series, b: pd.Series, alpha: float = 0.05,
                      question: str = "") -> TestResult:
    a, b = a.dropna().astype(float), b.dropna().astype(float)
    var_a, var_b = a.var(ddof=1), b.var(ddof=1)
    f_stat = var_a / var_b if var_a > var_b else var_b / var_a
    df1, df2 = (len(a) - 1, len(b) - 1) if var_a > var_b else (len(b) - 1, len(a) - 1)
    p = 2 * min(sps.f.cdf(f_stat, df1, df2), 1 - sps.f.cdf(f_stat, df1, df2))
    crit = sps.f.ppf(1 - alpha / 2, df1, df2)
    return TestResult(
        research_question=question or "Do the two groups have equal variances?",
        h0="var_a = var_b", h1="var_a != var_b", alpha=alpha,
        assumptions=["Independent samples", "Normally distributed populations"],
        test_statistic=float(f_stat), df_=(df1, df2), p_value=float(p), critical_value=float(crit),
        extra={"var_a": float(var_a), "var_b": float(var_b)},
    )
