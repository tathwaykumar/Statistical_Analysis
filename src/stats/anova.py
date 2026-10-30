"""Module F: ANOVA with mandatory sum-of-squares decomposition validation."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def one_way_anova(df: pd.DataFrame, value_col: str, group_col: str, alpha: float = 0.05) -> dict:
    data = df[[value_col, group_col]].dropna()
    groups = [g[value_col].to_numpy(dtype=float) for _, g in data.groupby(group_col)]
    group_names = list(data.groupby(group_col).groups.keys())

    f_stat, p_value = sps.f_oneway(*groups)

    grand_mean = data[value_col].mean()
    n_total = len(data)
    k = len(groups)

    ssb = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ssw = sum(((g - g.mean()) ** 2).sum() for g in groups)
    sst = ((data[value_col] - grand_mean) ** 2).sum()

    df_between, df_within = k - 1, n_total - k
    msb, msw = ssb / df_between, ssw / df_within
    f_recomputed = msb / msw
    f_critical = sps.f.ppf(1 - alpha, df_between, df_within)
    eta_squared = ssb / sst

    decomposition_ok = np.isclose(sst, ssb + ssw, rtol=1e-6)
    f_cross_check_ok = np.isclose(f_stat, f_recomputed, rtol=1e-6)

    group_stats = data.groupby(group_col)[value_col].agg(["count", "mean", "std"]).to_dict("index")

    tukey = None
    if p_value < alpha and k > 2:
        tukey_res = pairwise_tukeyhsd(data[value_col], data[group_col], alpha=alpha)
        tukey = pd.DataFrame(
            data=tukey_res._results_table.data[1:],
            columns=tukey_res._results_table.data[0],
        )

    levene_stat, levene_p = sps.levene(*groups)

    return {
        "value_col": value_col, "group_col": group_col, "groups": group_names,
        "k_groups": k, "n_total": n_total, "grand_mean": float(grand_mean),
        "ssb": float(ssb), "ssw": float(ssw), "sst": float(sst),
        "df_between": df_between, "df_within": df_within,
        "msb": float(msb), "msw": float(msw),
        "f_statistic": float(f_stat), "f_recomputed": float(f_recomputed),
        "f_critical": float(f_critical), "p_value": float(p_value),
        "eta_squared": float(eta_squared),
        "decomposition_valid": bool(decomposition_ok),
        "f_cross_check_valid": bool(f_cross_check_ok),
        "reject_h0": bool(p_value < alpha),
        "group_stats": group_stats,
        "levene_statistic": float(levene_stat), "levene_p_value": float(levene_p),
        "variance_homogeneity_ok_at_0.05": bool(levene_p > 0.05),
        "tukey_posthoc": tukey,
    }


def welch_anova(df: pd.DataFrame, value_col: str, group_col: str, alpha: float = 0.05) -> dict:
    """Welch's ANOVA, recommended when the homogeneity-of-variance assumption fails."""
    data = df[[value_col, group_col]].dropna()
    groups = [g[value_col].to_numpy(dtype=float) for _, g in data.groupby(group_col)]
    res = sps.alexandergovern(*groups)
    return {
        "test": "Welch/Alexander-Govern ANOVA (variance-robust alternative)",
        "statistic": float(res.statistic), "p_value": float(res.pvalue),
        "reject_h0": bool(res.pvalue < alpha),
    }


def two_way_anova(df: pd.DataFrame, value_col: str, factor_a: str, factor_b: str) -> pd.DataFrame:
    data = df[[value_col, factor_a, factor_b]].dropna().rename(
        columns={value_col: "value", factor_a: "factor_a", factor_b: "factor_b"}
    )
    model = ols("value ~ C(factor_a) + C(factor_b) + C(factor_a):C(factor_b)", data=data).fit()
    table = anova_lm(model, typ=2)
    return table
