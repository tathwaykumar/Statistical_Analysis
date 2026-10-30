import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_data, identity_footer, page_header  # noqa: E402
from src.report.findings import compute_all_findings  # noqa: E402

st.set_page_config(page_title="Research Findings", layout="wide")
page_header("Research Findings")
identity_footer()

df, _ = get_data()
findings = compute_all_findings(df)

st.caption("Every result below is computed live from the current cleaned dataset using the same "
           "statistical engine that generates the PDF report — the two are always consistent.")

for f in findings:
    with st.container(border=True):
        st.markdown(f"**{f['id']}. {f['question']}**")
        st.caption(f"Method: {f['method']}")
        st.write(f["result"])
