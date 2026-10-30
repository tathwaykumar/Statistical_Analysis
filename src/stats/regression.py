"""Module D: linear regression with diagnostics, VIF and train/test evaluation."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats as sps
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor


def fit_ols(df: pd.DataFrame, target: str, predictors: list[str]) -> dict:
    """Fit OLS regression (simple if one predictor, multiple otherwise)."""
    data = df[[target] + predictors].dropna()
    X = sm.add_constant(data[predictors])
    y = data[target]
    model = sm.OLS(y, X).fit()

    vif = {}
    if len(predictors) > 1:
        for i, col in enumerate(predictors):
            vif[col] = float(variance_inflation_factor(X.values, i + 1))

    return {
        "target": target,
        "predictors": predictors,
        "n": int(model.nobs),
        "intercept": float(model.params["const"]),
        "coefficients": {p: float(model.params[p]) for p in predictors},
        "p_values": {p: float(model.pvalues[p]) for p in predictors},
        "std_errors": {p: float(model.bse[p]) for p in predictors},
        "r_squared": float(model.rsquared),
        "adj_r_squared": float(model.rsquared_adj),
        "f_statistic": float(model.fvalue),
        "f_p_value": float(model.f_pvalue),
        "residuals": model.resid.to_numpy(),
        "fitted": model.fittedvalues.to_numpy(),
        "vif": vif,
        "_model": model,
    }


def train_test_evaluation(df: pd.DataFrame, target: str, predictors: list[str],
                           test_size: float = 0.2, random_state: int = 42) -> dict:
    data = df[[target] + predictors].dropna()
    X, y = data[predictors], data[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    X_train_c = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train_c).fit()
    X_test_c = sm.add_constant(X_test, has_constant="add")
    y_pred = model.predict(X_test_c)

    mse = mean_squared_error(y_test, y_pred)
    return {
        "n_train": len(X_train),
        "n_test": len(X_test),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "mse": float(mse),
        "rmse": float(np.sqrt(mse)),
        "r2_test": float(r2_score(y_test, y_pred)),
        "y_test": y_test.to_numpy(),
        "y_pred": y_pred.to_numpy(),
    }


def residual_diagnostics(residuals: np.ndarray, fitted: np.ndarray) -> dict:
    """Checks for residual normality (Shapiro) and homoscedasticity proxy (Breusch-Pagan-lite)."""
    shapiro_stat, shapiro_p = sps.shapiro(residuals)
    corr_abs_resid_fitted = float(np.corrcoef(np.abs(residuals), fitted)[0, 1])
    return {
        "residual_mean": float(np.mean(residuals)),
        "shapiro_statistic": float(shapiro_stat),
        "shapiro_p_value": float(shapiro_p),
        "residuals_normal_at_0.05": bool(shapiro_p > 0.05),
        "abs_resid_vs_fitted_corr": corr_abs_resid_fitted,
        "homoscedasticity_flag": (
            "no strong heteroscedasticity signal"
            if abs(corr_abs_resid_fitted) < 0.3
            else "possible heteroscedasticity - |corr| >= 0.3"
        ),
    }
