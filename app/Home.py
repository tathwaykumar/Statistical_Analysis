import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.common import get_data, identity_footer, page_header  # noqa: E402
from config.student_config import (  # noqa: E402
    STUDENT_NAME, UNIVERSITY, PROGRAMME, SPECIALIZATION, COURSE_NAME,
    ACADEMIC_SEMESTER, REGISTRATION_NUMBER, FACULTY_NAME,
)
from src.stats import correlation, hypothesis, anova, regression  # noqa: E402

st.set_page_config(page_title="Statistical Data Analysis Platform", layout="wide",
                    initial_sidebar_state="expanded")
page_header("Executive Overview")
identity_footer()

df, report = get_data()

st.markdown(f"#### {STUDENT_NAME} &nbsp;·&nbsp; {PROGRAMME} ({SPECIALIZATION})")
st.caption(f"{UNIVERSITY} · {COURSE_NAME} · {ACADEMIC_SEMESTER} · Reg. No. {REGISTRATION_NUMBER} · "
           f"Faculty: {FACULTY_NAME}")

st.markdown("##### Dataset: UCI Student Performance (Math + Portuguese courses)")
st.caption("Source: P. Cortez & A. Silva (2008), UCI Machine Learning Repository. "
           "Real survey + school-record data from two Portuguese secondary schools.")

c1, c2, c3, c4 = st.columns(4)
for col, label, value in zip(
    [c1, c2, c3, c4],
    ["Observations", "Variables", "Missing Values", "Duplicate Rows Removed"],
    [len(df), df.shape[1], f"{df.isna().sum().sum()} ({df.isna().sum().sum()/df.size*100:.1f}%)",
     report.duplicates_dropped],
):
    col.markdown(
        f'<div class="stat-card"><div class="label">{label}</div>'
        f'<div class="value">{value}</div></div>', unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("##### Key statistical findings (computed live from the current dataset)")

k1, k2, k3 = st.columns(3)
with k1:
    corr = correlation.pairwise_correlation(df["studytime"], df["G3"])
    st.markdown(
        f'<div class="stat-card"><div class="label">Correlation: studytime vs G3</div>'
        f'<div class="value">r = {corr["r"]:.3f}</div>'
        f'<div>{corr["strength"]} · p = {corr["p_value"]:.4f}</div></div>',
        unsafe_allow_html=True,
    )
with k2:
    reg = regression.fit_ols(df, "G3", ["G1", "G2", "absences"])
    st.markdown(
        f'<div class="stat-card"><div class="label">Regression: predicting G3</div>'
        f'<div class="value">R² = {reg["r_squared"]:.3f}</div>'
        f'<div>Predictors: G1, G2, absences</div></div>',
        unsafe_allow_html=True,
    )
with k3:
    av = anova.one_way_anova(df, "G3", "Mjob")
    st.markdown(
        f'<div class="stat-card"><div class="label">ANOVA: G3 across Mjob groups</div>'
        f'<div class="value">F = {av["f_statistic"]:.2f}</div>'
        f'<div>p = {av["p_value"]:.4g} · '
        f'{"significant" if av["reject_h0"] else "not significant"} at 0.05</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("##### Navigate")
st.caption(
    "Use the sidebar page list to move between Dataset Explorer, Data Quality & Cleaning, "
    "Descriptive Statistics, Probability & Distributions, Correlation Analysis, Regression "
    "Analysis, Hypothesis Testing, ANOVA, Interactive Visualizations, Research Findings, "
    "Report Generation and About the Project."
)
