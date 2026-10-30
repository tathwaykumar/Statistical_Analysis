import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import NUMERIC_COLUMNS, CATEGORICAL_COLUMNS, get_data, identity_footer, page_header  # noqa: E402
from src.stats.descriptive import numeric_summary, frequency_table  # noqa: E402
from src.visualization.plots import histogram, box_plot, density_plot  # noqa: E402

st.set_page_config(page_title="Descriptive Statistics", layout="wide")
page_header("Descriptive Statistics")
identity_footer()

df, _ = get_data()

tab1, tab2 = st.tabs(["Numeric variables", "Categorical variables"])

with tab1:
    col = st.selectbox("Select a numeric variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
    summary = numeric_summary(df[col])
    cols = st.columns(4)
    labels = ["n", "mean", "median", "mode", "std", "variance", "range", "iqr"]
    for i, lab in enumerate(labels):
        cols[i % 4].markdown(
            f'<div class="stat-card"><div class="label">{lab}</div>'
            f'<div class="value">{summary[lab]:.3f}</div></div>', unsafe_allow_html=True
        )
    st.caption(f"Skewness: {summary['skewness']:.3f} · Kurtosis (excess): {summary['kurtosis']:.3f} "
               f"· Q1: {summary['q1']} · Q3: {summary['q3']} · Min: {summary['min']} · Max: {summary['max']}")

    c1, c2, c3 = st.columns(3)
    c1.plotly_chart(histogram(df, col), use_container_width=True, theme=None)
    c2.plotly_chart(box_plot(df, col), use_container_width=True, theme=None)
    c3.plotly_chart(density_plot(df, col), use_container_width=True, theme=None)

with tab2:
    col = st.selectbox("Select a categorical variable", CATEGORICAL_COLUMNS)
    freq = frequency_table(df[col])
    st.dataframe(freq, use_container_width=True)
    st.bar_chart(freq["count"])
