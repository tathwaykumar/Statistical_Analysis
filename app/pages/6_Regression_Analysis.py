import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import NUMERIC_COLUMNS, get_data, identity_footer, page_header  # noqa: E402
from src.stats import regression  # noqa: E402
from src.visualization.plots import residual_plot, predicted_vs_actual  # noqa: E402

st.set_page_config(page_title="Regression Analysis", layout="wide")
page_header("Regression Analysis")
identity_footer()

df, _ = get_data()
predictor_pool = [c for c in NUMERIC_COLUMNS if c != "G3"]

target = st.selectbox("Target variable", ["G3", "average_grade"])
predictors = st.multiselect("Predictor variable(s)", [c for c in NUMERIC_COLUMNS if c != target],
                             default=["G1", "G2", "studytime", "absences"])

if predictors:
    result = regression.fit_ols(df, target, predictors)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("R²", f"{result['r_squared']:.3f}")
    c2.metric("Adjusted R²", f"{result['adj_r_squared']:.3f}")
    c3.metric("F-statistic", f"{result['f_statistic']:.2f}")
    c4.metric("F p-value", f"{result['f_p_value']:.4g}")

    st.markdown("##### Coefficients")
    st.dataframe({
        "predictor": predictors,
        "coefficient": [f"{result['coefficients'][p]:.4f}" for p in predictors],
        "std_error": [f"{result['std_errors'][p]:.4f}" for p in predictors],
        "p_value": [f"{result['p_values'][p]:.4g}" for p in predictors],
        "VIF": [f"{result['vif'][p]:.3f}" if p in result["vif"] else "n/a" for p in predictors],
    }, use_container_width=True)
    st.caption(f"Intercept: {result['intercept']:.4f}. Equation: {target} = {result['intercept']:.3f} + "
               + " + ".join(f"{result['coefficients'][p]:.3f}*{p}" for p in predictors))
    if any(v != "n/a" and v > 5 for v in result["vif"].values()):
        st.warning("VIF > 5 detected for at least one predictor — possible multicollinearity.")

    st.markdown("---")
    st.markdown("##### Residual diagnostics")
    diag = regression.residual_diagnostics(result["residuals"], result["fitted"])
    st.json(diag)
    c1, c2 = st.columns(2)
    c1.plotly_chart(residual_plot(result["fitted"], result["residuals"]), use_container_width=True, theme=None)
    c2.plotly_chart(predicted_vs_actual(df.loc[df[[target] + predictors].dropna().index, target].to_numpy(),
                                         result["fitted"]), use_container_width=True, theme=None)

    st.markdown("---")
    st.markdown("##### Train/test evaluation")
    test_size = st.slider("Test set proportion", 0.1, 0.4, 0.2, 0.05)
    tt = regression.train_test_evaluation(df, target, predictors, test_size=test_size)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("MAE", f"{tt['mae']:.3f}")
    c2.metric("MSE", f"{tt['mse']:.3f}")
    c3.metric("RMSE", f"{tt['rmse']:.3f}")
    c4.metric("Test R²", f"{tt['r2_test']:.3f}")

    st.info("Regression quantifies association between predictors and the target under the model's "
            "assumptions — it does not, by itself, establish causation.")
else:
    st.warning("Select at least one predictor.")
