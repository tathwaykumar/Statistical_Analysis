import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS, get_data, identity_footer, page_header  # noqa: E402
from src.visualization.plots import style_figure  # noqa: E402

st.set_page_config(page_title="Interactive Visualizations", layout="wide")
page_header("Interactive Visualizations")
identity_footer()

df, _ = get_data()

chart_type = st.selectbox("Chart type", ["Scatter", "Box", "Violin", "Bar (grouped mean)", "Pair plot"])

if chart_type == "Scatter":
    c1, c2, c3 = st.columns(3)
    x = c1.selectbox("X", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("studytime"))
    y = c2.selectbox("Y", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
    color = c3.selectbox("Color by", [None] + CATEGORICAL_COLUMNS)
    fig = px.scatter(df, x=x, y=y, color=color, opacity=0.7, trendline="ols",
                      color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(style_figure(fig, f"{y} vs {x}"), use_container_width=True, theme=None)

elif chart_type == "Box":
    c1, c2 = st.columns(2)
    y = c1.selectbox("Numeric variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
    x = c2.selectbox("Group by", CATEGORICAL_COLUMNS)
    fig = px.box(df, x=x, y=y, color=x, color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(style_figure(fig, f"{y} by {x}"), use_container_width=True, theme=None)

elif chart_type == "Violin":
    c1, c2 = st.columns(2)
    y = c1.selectbox("Numeric variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
    x = c2.selectbox("Group by", CATEGORICAL_COLUMNS)
    fig = px.violin(df, x=x, y=y, color=x, box=True, color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(style_figure(fig, f"{y} by {x}"), use_container_width=True, theme=None)

elif chart_type == "Bar (grouped mean)":
    c1, c2 = st.columns(2)
    y = c1.selectbox("Numeric variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
    x = c2.selectbox("Group by", CATEGORICAL_COLUMNS)
    grouped = df.groupby(x)[y].mean().reset_index()
    fig = px.bar(grouped, x=x, y=y, color=x, color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(style_figure(fig, f"Mean {y} by {x}"), use_container_width=True, theme=None)

else:
    cols = st.multiselect("Variables for pair plot", NUMERIC_COLUMNS,
                           default=["studytime", "absences", "G1", "G2", "G3"])
    if 2 <= len(cols) <= 6:
        fig = px.scatter_matrix(df, dimensions=cols, color="sex",
                                 color_discrete_sequence=px.colors.qualitative.Safe)
        fig = style_figure(fig, "Pair plot")
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True, theme=None)
    else:
        st.warning("Select between 2 and 6 variables.")
