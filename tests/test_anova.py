import numpy as np
import pandas as pd
from scipy import stats as sps

from src.stats.anova import one_way_anova


def test_sst_equals_ssb_plus_ssw():
    """Mandatory mathematical validation: SST = SSB + SSW."""
    df = pd.DataFrame({
        "value": [23, 25, 21, 30, 32, 29, 18, 20, 19],
        "group": ["A"] * 3 + ["B"] * 3 + ["C"] * 3,
    })
    result = one_way_anova(df, "value", "group")
    assert np.isclose(result["sst"], result["ssb"] + result["ssw"])
    assert result["decomposition_valid"] is True


def test_f_statistic_matches_scipy_f_oneway():
    df = pd.DataFrame({
        "value": [23, 25, 21, 30, 32, 29, 18, 20, 19, 24, 26, 22],
        "group": ["A"] * 4 + ["B"] * 4 + ["C"] * 4,
    })
    result = one_way_anova(df, "value", "group")
    groups = [g["value"].to_numpy() for _, g in df.groupby("group")]
    expected_f, expected_p = sps.f_oneway(*groups)
    assert np.isclose(result["f_statistic"], expected_f)
    assert np.isclose(result["p_value"], expected_p)
    assert np.isclose(result["f_statistic"], result["f_recomputed"])


def test_degrees_of_freedom_correct():
    df = pd.DataFrame({
        "value": list(range(30)),
        "group": ["A"] * 10 + ["B"] * 10 + ["C"] * 10,
    })
    result = one_way_anova(df, "value", "group")
    assert result["df_between"] == 2  # k - 1 = 3 - 1
    assert result["df_within"] == 27  # n - k = 30 - 3
