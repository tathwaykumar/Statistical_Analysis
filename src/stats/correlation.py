"""Module C: correlation analysis (Pearson & Spearman) with significance testing."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps


def pairwise_correlation(x: pd.Series, y: pd.Series, method: str = "pearson") -> dict:
    """Correlation coefficient, p-value and 95% CI (Fisher z, Pearson only)."""
    x, y = pd.to_numeric(x), pd.to_numeric(y)
    valid = x.notna() & y.notna()
    x, y = x[valid], y[valid]
    n = len(x)

    if method == "pearson":
        r, p = sps.pearsonr(x, y)
    elif method == "spearman":
        r, p = sps.spearmanr(x, y)
    else:
        raise ValueError("method must be 'pearson' or 'spearman'")

    ci_low, ci_high = None, None
    if method == "pearson" and n > 3 and abs(r) < 1:
        z = np.arctanh(r)
        se = 1 / np.sqrt(n - 3)
        z_low, z_high = z - 1.96 * se, z + 1.96 * se
        ci_low, ci_high = float(np.tanh(z_low)), float(np.tanh(z_high))

    return {
        "method": method,
        "n": n,
        "r": float(r),
        "p_value": float(p),
        "ci_95_low": ci_low,
        "ci_95_high": ci_high,
        "strength": interpret_strength(r),
        "significant_at_0.05": bool(p < 0.05),
    }


def interpret_strength(r: float) -> str:
    a = abs(r)
    if a < 0.1:
        return "negligible"
    if a < 0.3:
        return "weak"
    if a < 0.5:
        return "moderate"
    if a < 0.7:
        return "strong"
    return "very strong"


def correlation_matrix(df: pd.DataFrame, columns: list[str], method: str = "pearson") -> pd.DataFrame:
    return df[columns].corr(method=method)


def correlation_pvalue_matrix(df: pd.DataFrame, columns: list[str], method: str = "pearson") -> pd.DataFrame:
    n = len(columns)
    pvals = pd.DataFrame(np.ones((n, n)), index=columns, columns=columns)
    for i, a in enumerate(columns):
        for j, b in enumerate(columns):
            if i >= j:
                continue
            res = pairwise_correlation(df[a], df[b], method=method)
            pvals.loc[a, b] = pvals.loc[b, a] = res["p_value"]
    return pvals
