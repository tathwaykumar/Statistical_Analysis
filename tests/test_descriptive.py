import numpy as np
import pandas as pd

from src.stats.descriptive import numeric_summary


def test_numeric_summary_against_manual_calculation():
    s = pd.Series([2, 4, 4, 4, 5, 5, 7, 9])
    out = numeric_summary(s)
    assert np.isclose(out["mean"], s.mean())
    assert np.isclose(out["median"], s.median())
    assert np.isclose(out["std"], s.std(ddof=1))
    assert np.isclose(out["variance"], s.var(ddof=1))
    assert np.isclose(out["range"], s.max() - s.min())
    assert out["mode"] == 4.0


def test_known_textbook_dataset():
    # Classic textbook example with known population values.
    s = pd.Series([10, 12, 23, 23, 16, 23, 21, 16])
    out = numeric_summary(s)
    assert np.isclose(out["mean"], 18.0)
    assert out["mode"] == 23.0
