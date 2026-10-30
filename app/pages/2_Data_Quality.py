import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_data, identity_footer, page_header  # noqa: E402

st.set_page_config(page_title="Data Quality & Cleaning", layout="wide")
page_header("Data Quality & Cleaning")
identity_footer()

df, report = get_data()

st.markdown("##### Cleaning log")
for step in report.steps:
    st.markdown(f"- {step}")

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.markdown("##### Missing values before cleaning")
    st.dataframe({"column": list(report.missing_before.keys()),
                  "missing_count": list(report.missing_before.values())}, use_container_width=True)
with c2:
    st.markdown("##### Duplicate rows")
    st.metric("Exact duplicate rows found", report.duplicates_found)
    st.metric("Rows before cleaning", report.rows_before)
    st.metric("Rows after cleaning", report.rows_after)

st.markdown("---")
st.markdown("##### Student overlap between subject files (independence caveat)")
ov = report.subject_overlap
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overlapping students", ov["n_overlapping_students"])
c2.metric("Math-only students", ov["n_math_only_students"])
c3.metric("Portuguese-only students", ov["n_portuguese_only_students"])
c4.metric("Unique students (est.)", ov["n_unique_students_estimate"])
st.warning(
    f"The combined dataset has {ov['n_combined_rows']} rows, but only an estimated "
    f"{ov['n_unique_students_estimate']} unique students — {ov['n_overlapping_students']} of the "
    f"{ov['n_math_rows']} Math students also appear in the Portuguese file (identified using the "
    "dataset authors' own merge key from student-merge.R). Any analysis comparing the two subjects "
    "directly (e.g. the Math-vs-Portuguese F-test on this platform) is therefore comparing "
    "substantially overlapping, non-independent samples, and its 'independent samples' assumption "
    "should be read with this caveat in mind."
)

st.markdown("---")
st.markdown("##### Flagged outliers (IQR rule) — retained, not removed")
st.caption("Extreme values are legitimate observations (e.g. 93 absences is a real recorded value); "
           "removing them would bias estimates, so they are flagged for awareness only.")
st.dataframe({"column": list(report.outliers.keys()),
              "outlier_count": list(report.outliers.values())}, use_container_width=True)
