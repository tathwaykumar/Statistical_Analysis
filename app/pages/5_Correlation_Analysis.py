import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import NUMERIC_COLUMNS, get_data, identity_footer, page_header  # noqa: E402
from src.stats import correlation  # noqa: E402
from src.visualization.plots import correlation_heatmap, scatter_with_trendline  # noqa: E402

st.set_page_config(page_title="Correlation Analysis", layout="wide")
page_header("Correlation Analysis")
identity_footer()

df, _ = get_data()

st.markdown("##### Correlation matrix")
method = st.radio("Method", ["pearson", "spearman"], horizontal=True)
selected_cols = st.multiselect("Variables", NUMERIC_COLUMNS,
                                default=["studytime", "failures", "absences", "G1", "G2", "G3"])
if len(selected_cols) >= 2:
    cm = correlation.correlation_matrix(df, selected_cols, method=method)
    st.plotly_chart(correlation_heatmap(cm, f"{method.title()} correlation heatmap"), use_container_width=True, theme=None)

    st.markdown("---")
    st.markdown("##### Pairwise correlation with significance testing")
    c1, c2 = st.columns(2)
    x = c1.selectbox("Variable X", selected_cols, index=0)
    y = c2.selectbox("Variable Y", selected_cols, index=len(selected_cols) - 1)
    result = correlation.pairwise_correlation(df[x], df[y], method=method)
    cols = st.columns(4)
    cols[0].metric("r", f"{result['r']:.3f}")
    cols[1].metric("p-value", f"{result['p_value']:.4g}")
    cols[2].metric("Strength", result["strength"])
    cols[3].metric("Significant (0.05)", "Yes" if result["significant_at_0.05"] else "No")
    if result["ci_95_low"] is not None:
        st.caption(f"95% CI for r: [{result['ci_95_low']:.3f}, {result['ci_95_high']:.3f}]")
    st.plotly_chart(scatter_with_trendline(df, x, y, color="sex"), use_container_width=True, theme=None)
    st.info("Correlation measures linear association, not causation. A significant r between "
            "two variables does not prove one causes the other.")
else:
    st.warning("Select at least two variables.")
