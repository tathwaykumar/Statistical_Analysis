import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import identity_footer, page_header  # noqa: E402
from config.student_config import (  # noqa: E402
    ACADEMIC_SEMESTER, COURSE_NAME, FACULTY_NAME, PROGRAMME, REGISTRATION_NUMBER,
    SPECIALIZATION, STUDENT_NAME, UNIVERSITY,
)

st.set_page_config(page_title="About the Project", layout="wide")
page_header("About the Project")
identity_footer()

st.markdown(f"""
**Student:** {STUDENT_NAME}
**Registration Number:** {REGISTRATION_NUMBER}
**Programme:** {PROGRAMME} ({SPECIALIZATION})
**University:** {UNIVERSITY}
**Course:** {COURSE_NAME}
**Semester:** {ACADEMIC_SEMESTER}
**Faculty:** {FACULTY_NAME}

This is an independent, additional-learning project. It has not been submitted for or claimed to
receive any academic credit, approval or endorsement.

#### Dataset
UCI Machine Learning Repository — "Student Performance" dataset (Cortez & Silva, 2008).
Two real secondary-school cohorts (Math: 395 students, Portuguese: 649 students), combined into a
1,044-row dataset with 38 variables (demographic, behavioural, academic-history and grade variables).

#### Technology stack
Python, Pandas, NumPy, SciPy, Statsmodels, scikit-learn, Streamlit, Plotly, Matplotlib, ReportLab, Pytest.

#### Integrity commitments
- No data is simulated or fabricated; the raw UCI files are preserved untouched in `data/raw/`.
- Every statistic shown in the dashboard and the PDF report is computed live from the same code path.
- ANOVA's sum-of-squares decomposition (SST = SSB + SSW) is mathematically re-verified on every run.
- Automated tests independently cross-check descriptive, correlation, regression and ANOVA calculations.
""")
