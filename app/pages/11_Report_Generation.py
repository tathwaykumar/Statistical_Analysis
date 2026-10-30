import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_data, identity_footer, page_header  # noqa: E402
from config.student_config import EXPORTS_DIR, REPORTS_DIR  # noqa: E402
from src.report.pdf_report import build_report  # noqa: E402

st.set_page_config(page_title="Report Generation", layout="wide")
page_header("Report Generation")
identity_footer()

df, report = get_data()

st.markdown("##### Academic PDF report")
st.caption("Regenerates the full report directly from the current dataset and statistical engine, "
           "guaranteeing it matches every number shown on this dashboard.")

if st.button("Generate PDF report", type="primary"):
    with st.spinner("Building report..."):
        out_path = REPORTS_DIR / "Statistical_Data_Analysis_Report.pdf"
        build_report(out_path)
    st.success(f"Report generated: {out_path}")
    with open(out_path, "rb") as f:
        st.download_button("Download PDF report", f.read(), file_name=out_path.name, mime="application/pdf")

st.markdown("---")
st.markdown("##### Data & results export")
c1, c2 = st.columns(2)
with c1:
    st.download_button("Download cleaned dataset (CSV)", df.to_csv(index=False).encode("utf-8"),
                        file_name="student_performance_clean.csv", mime="text/csv")
with c2:
    st.download_button("Download cleaning log (TXT)", "\n".join(report.steps).encode("utf-8"),
                        file_name="cleaning_log.txt", mime="text/plain")
