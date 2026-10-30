import numpy as np
import pandas as pd
from scipy import stats as sps

from src.stats.hypothesis import (
    chi_square_independence, one_sample_ttest, paired_ttest, two_sample_ttest,
)


def test_one_sample_ttest_matches_scipy():
    s = pd.Series([5, 7, 8, 6, 9, 7, 6, 8, 7, 5])
    result = one_sample_ttest(s, popmean=6)
    expected_stat, expected_p = sps.ttest_1samp(s, 6)
    assert np.isclose(result.test_statistic, expected_stat)
    assert np.isclose(result.p_value, expected_p)
    assert result.decision in {"Reject H0", "Fail to reject H0"}


def test_two_sample_ttest_matches_scipy_equal_var():
    a = pd.Series([23, 21, 18, 25, 20])
    b = pd.Series([30, 28, 32, 27, 29])
    result = two_sample_ttest(a, b, equal_var=True)
    expected_stat, expected_p = sps.ttest_ind(a, b, equal_var=True)
    assert np.isclose(result.test_statistic, expected_stat)
    assert np.isclose(result.p_value, expected_p)
    assert result.reject_h0 is True  # clearly separated groups


def test_paired_ttest_matches_scipy():
    before = pd.Series([10, 12, 9, 15, 11])
    after = pd.Series([12, 13, 10, 17, 14])
    result = paired_ttest(before, after)
    expected_stat, expected_p = sps.ttest_rel(after, before)
    assert np.isclose(result.test_statistic, expected_stat)
    assert np.isclose(result.p_value, expected_p)


def test_chi_square_independence_matches_scipy():
    df = pd.DataFrame({
        "a": ["x"] * 20 + ["y"] * 20,
        "b": ["p"] * 15 + ["q"] * 5 + ["p"] * 5 + ["q"] * 15,
    })
    table = pd.crosstab(df["a"], df["b"])
    expected_stat, expected_p, expected_dof, _ = sps.chi2_contingency(table)
    result = chi_square_independence(df, "a", "b")
    assert np.isclose(result.test_statistic, expected_stat)
    assert np.isclose(result.p_value, expected_p)
    assert result.df_ == expected_dof
