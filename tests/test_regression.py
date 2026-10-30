import numpy as np
import pandas as pd

from src.stats.regression import fit_ols


def test_simple_regression_recovers_known_linear_relationship():
    rng = np.random.default_rng(7)
    x = rng.uniform(0, 10, size=300)
    y = 3.0 + 2.0 * x + rng.normal(scale=0.1, size=300)
    df = pd.DataFrame({"x": x, "y": y})
    result = fit_ols(df, "y", ["x"])
    assert np.isclose(result["intercept"], 3.0, atol=0.2)
    assert np.isclose(result["coefficients"]["x"], 2.0, atol=0.05)
    assert result["r_squared"] > 0.99


def test_r_squared_matches_manual_calculation():
    rng = np.random.default_rng(3)
    x = rng.uniform(0, 5, size=150)
    y = 1 + 4 * x + rng.normal(scale=2, size=150)
    df = pd.DataFrame({"x": x, "y": y})
    result = fit_ols(df, "y", ["x"])

    fitted = result["fitted"]
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    manual_r2 = 1 - ss_res / ss_tot
    assert np.isclose(result["r_squared"], manual_r2, atol=1e-6)
