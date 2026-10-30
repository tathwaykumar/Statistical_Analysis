import sys
from pathlib import Path

import numpy as np
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import NUMERIC_COLUMNS, get_data, identity_footer, page_header  # noqa: E402
from src.stats import probability  # noqa: E402
from src.visualization.plots import density_plot  # noqa: E402

st.set_page_config(page_title="Probability & Distributions", layout="wide")
page_header("Probability & Distributions")
identity_footer()

df, _ = get_data()

st.markdown("##### Empirical, conditional & joint probability")
c1, c2 = st.columns(2)
with c1:
    p_pass = probability.empirical_probability(df["pass_fail"], "Pass")
    st.markdown(f'<div class="stat-card"><div class="label">P(Pass), overall</div>'
                f'<div class="value">{p_pass:.3f}</div></div>', unsafe_allow_html=True)
    p_pass_given_higher = probability.conditional_probability(df, "pass_fail", "Pass", "higher", True)
    st.markdown(f'<div class="stat-card"><div class="label">P(Pass | wants higher education)</div>'
                f'<div class="value">{p_pass_given_higher:.3f}</div></div>', unsafe_allow_html=True)
with c2:
    p_pass_internet = probability.conditional_probability(df, "pass_fail", "Pass", "internet", True)
    st.markdown(f'<div class="stat-card"><div class="label">P(Pass | has internet at home)</div>'
                f'<div class="value">{p_pass_internet:.3f}</div></div>', unsafe_allow_html=True)
    joint = probability.joint_probability(df, "pass_fail", "Pass", "sex", "F")
    st.markdown(f'<div class="stat-card"><div class="label">P(Pass AND Female)</div>'
                f'<div class="value">{joint:.3f}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("##### Bayes' theorem — P(wants higher ed | Pass)")
p_higher = probability.empirical_probability(df["higher"], True)
p_pass_given_higher = probability.conditional_probability(df, "pass_fail", "Pass", "higher", True)
bayes_result = probability.bayes_theorem(p_pass_given_higher, p_higher, p_pass)
st.latex(r"P(\text{higher}\mid\text{Pass}) = \frac{P(\text{Pass}\mid\text{higher}) \cdot P(\text{higher})}{P(\text{Pass})}")
st.write(f"= ({p_pass_given_higher:.3f} × {p_higher:.3f}) / {p_pass:.3f} = **{bayes_result:.3f}**")

st.markdown("---")
st.markdown("##### Normality assessment & distribution fitting")
col = st.selectbox("Variable", NUMERIC_COLUMNS, index=NUMERIC_COLUMNS.index("G3"))
norm_test = probability.normality_assessment(df[col])
fit = probability.fit_normal(df[col])
c1, c2 = st.columns(2)
c1.json(norm_test)
c2.json(fit)
st.plotly_chart(density_plot(df, col), use_container_width=True, theme=None)
st.caption("Shapiro-Wilk H0: the variable is normally distributed. A small p-value (< alpha) means "
           "we reject normality — common for bounded, skewed grade/count data such as this.")
