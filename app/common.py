"""Shared Streamlit helpers: data loading, theming, header component."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config.student_config import (  # noqa: E402
    PROJECT_TITLE, PROJECT_SUBTITLE, STUDENT_NAME, UNIVERSITY, PROGRAMME,
    SPECIALIZATION, COURSE_NAME, ACADEMIC_SEMESTER, REGISTRATION_NUMBER,
    FACULTY_NAME, DEFAULT_SIGNIFICANCE_LEVEL,
)
from src.data.clean import clean_dataset  # noqa: E402

CUSTOM_CSS = """
<style>
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif; }
.block-container { padding-top: 2rem; max-width: 1200px; }
h1, h2, h3 { color: #0B1E3D; font-weight: 700; }
.stat-card {
    background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px;
    padding: 1.1rem 1.3rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.stat-card .label { color: #64748B; font-size: 0.80rem; text-transform: uppercase;
    letter-spacing: 0.04em; margin-bottom: 0.25rem; }
.stat-card .value { color: #0B1E3D; font-size: 1.6rem; font-weight: 700; }
.badge-pass { color: #15803D; background: #DCFCE7; padding: 2px 10px; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; }
.badge-fail { color: #B91C1C; background: #FEE2E2; padding: 2px 10px; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; }
.project-header { border-bottom: 1px solid #E5E7EB; padding-bottom: 1rem; margin-bottom: 1.3rem; }
section[data-testid="stSidebar"] { background: #0B1E3D; }
section[data-testid="stSidebar"] * { color: #E5E7EB !important; }
</style>
"""


def inject_css() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def page_header(subtitle: str | None = None) -> None:
    inject_css()
    st.markdown('<div class="project-header">', unsafe_allow_html=True)
    st.markdown(f"### {PROJECT_TITLE}")
    st.caption(subtitle or PROJECT_SUBTITLE)
    st.markdown("</div>", unsafe_allow_html=True)


def identity_footer() -> None:
    st.sidebar.markdown("---")
    st.sidebar.caption(f"**{STUDENT_NAME}**")
    st.sidebar.caption(f"{PROGRAMME} ({SPECIALIZATION})")
    st.sidebar.caption(UNIVERSITY)
    st.sidebar.caption(f"{COURSE_NAME} · {ACADEMIC_SEMESTER}")
    st.sidebar.caption(f"Reg. No.: {REGISTRATION_NUMBER}")
    st.sidebar.caption(f"Faculty: {FACULTY_NAME}")


@st.cache_data(show_spinner="Loading and validating dataset...")
def get_data():
    df, report = clean_dataset()
    return df, report


def get_alpha() -> float:
    if "alpha" not in st.session_state:
        st.session_state["alpha"] = DEFAULT_SIGNIFICANCE_LEVEL
    with st.sidebar:
        st.markdown("#### Significance level")
        st.session_state["alpha"] = st.select_slider(
            "alpha (used across all hypothesis tests & ANOVA)",
            options=[0.01, 0.05, 0.10], value=st.session_state["alpha"],
        )
    return st.session_state["alpha"]


NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences",
    "G1", "G2", "G3", "average_grade", "grade_trend",
]
CATEGORICAL_COLUMNS = [
    "subject", "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
    "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic", "pass_fail",
]
