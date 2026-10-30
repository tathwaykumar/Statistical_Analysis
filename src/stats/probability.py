"""Module B: probability and distribution analysis on real dataset variables."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps


def empirical_probability(series: pd.Series, condition) -> float:
    """P(condition) estimated empirically from observed frequencies."""
    mask = series.apply(condition) if callable(condition) else (series == condition)
    return float(mask.mean())


def conditional_probability(df: pd.DataFrame, event_col: str, event_val,
                             given_col: str, given_val) -> float:
    """P(event_col == event_val | given_col == given_val)."""
    subset = df[df[given_col] == given_val]
    if len(subset) == 0:
        return float("nan")
    return float((subset[event_col] == event_val).mean())


def joint_probability(df: pd.DataFrame, col_a: str, val_a, col_b: str, val_b) -> float:
    return float(((df[col_a] == val_a) & (df[col_b] == val_b)).mean())


def bayes_theorem(p_b_given_a: float, p_a: float, p_b: float) -> float:
    """P(A|B) = P(B|A) * P(A) / P(B)."""
    if p_b == 0:
        return float("nan")
    return p_b_given_a * p_a / p_b


def contingency_probabilities(df: pd.DataFrame, col_a: str, col_b: str) -> pd.DataFrame:
    """Joint probability table (relative frequencies) for two categorical columns."""
    ct = pd.crosstab(df[col_a], df[col_b], normalize="all")
    return ct


def normality_assessment(series: pd.Series) -> dict:
    """Shapiro-Wilk test for normality plus descriptive normality indicators."""
    s = series.dropna().astype(float)
    sample = s if len(s) <= 5000 else s.sample(5000, random_state=42)
    stat, p_value = sps.shapiro(sample)
    return {
        "test": "Shapiro-Wilk",
        "statistic": float(stat),
        "p_value": float(p_value),
        "is_normal_at_0.05": bool(p_value > 0.05),
        "skewness": float(sps.skew(s, bias=False)),
        "kurtosis_excess": float(sps.kurtosis(s, bias=False)),
    }


def fit_normal(series: pd.Series) -> dict:
    s = series.dropna().astype(float)
    mu, sigma = sps.norm.fit(s)
    return {"distribution": "normal", "mu": float(mu), "sigma": float(sigma)}


def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return sps.norm.pdf(x, loc=mu, scale=sigma)


def normal_cdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    return sps.norm.cdf(x, loc=mu, scale=sigma)
