"""Module A: descriptive statistics for numeric and categorical variables."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sps


def numeric_summary(series: pd.Series) -> dict:
    s = series.dropna().astype(float)
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    mode_result = s.mode()
    return {
        "n": int(s.count()),
        "mean": float(s.mean()),
        "median": float(s.median()),
        "mode": float(mode_result.iloc[0]) if not mode_result.empty else None,
        "min": float(s.min()),
        "max": float(s.max()),
        "range": float(s.max() - s.min()),
        "variance": float(s.var(ddof=1)),
        "std": float(s.std(ddof=1)),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "skewness": float(sps.skew(s, bias=False)),
        "kurtosis": float(sps.kurtosis(s, bias=False)),
    }


def dataset_overview(df: pd.DataFrame) -> dict:
    return {
        "n_observations": int(len(df)),
        "n_variables": int(df.shape[1]),
        "missing_total": int(df.isna().sum().sum()),
        "missing_pct": float(df.isna().sum().sum() / df.size * 100),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


def frequency_table(series: pd.Series) -> pd.DataFrame:
    counts = series.value_counts(dropna=False)
    pct = (counts / counts.sum() * 100).round(2)
    return pd.DataFrame({"count": counts, "percent": pct})


def all_numeric_summaries(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame({col: numeric_summary(df[col]) for col in columns}).T
