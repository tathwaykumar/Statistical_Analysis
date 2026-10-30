import numpy as np
import pandas as pd
from scipy import stats as sps

from src.stats.correlation import pairwise_correlation


def test_pearson_matches_scipy_directly():
    rng = np.random.default_rng(42)
    x = pd.Series(rng.normal(size=200))
    y = pd.Series(2 * x + rng.normal(scale=0.5, size=200))
    result = pairwise_correlation(x, y, method="pearson")
    expected_r, expected_p = sps.pearsonr(x, y)
    assert np.isclose(result["r"], expected_r)
    assert np.isclose(result["p_value"], expected_p)


def test_perfect_correlation_is_one():
    x = pd.Series(range(1, 21))
    y = pd.Series(range(1, 21))
    result = pairwise_correlation(x, y, method="pearson")
    assert np.isclose(result["r"], 1.0)
    assert result["strength"] == "very strong"


def test_confidence_interval_contains_point_estimate():
    rng = np.random.default_rng(1)
    x = pd.Series(rng.normal(size=100))
    y = pd.Series(x * 0.5 + rng.normal(scale=1, size=100))
    result = pairwise_correlation(x, y, method="pearson")
    assert result["ci_95_low"] < result["r"] < result["ci_95_high"]
