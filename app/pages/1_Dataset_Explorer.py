import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_data, identity_footer, page_header  # noqa: E402

st.set_page_config(page_title="Dataset Explorer", layout="wide")
page_header("Dataset Explorer")
identity_footer()

df, _ = get_data()

st.markdown("##### Filter the dataset")
c1, c2, c3 = st.columns(3)
subject = c1.multiselect("Subject", sorted(df["subject"].unique()), default=list(df["subject"].unique()))
sex = c2.multiselect("Sex", sorted(df["sex"].unique()), default=list(df["sex"].unique()))
school = c3.multiselect("School", sorted(df["school"].unique()), default=list(df["school"].unique()))

filtered = df[df["subject"].isin(subject) & df["sex"].isin(sex) & df["school"].isin(school)]
st.caption(f"Showing {len(filtered)} of {len(df)} observations after filtering.")

st.dataframe(filtered, use_container_width=True, height=420)

st.download_button(
    "Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_student_performance.csv", mime="text/csv",
)

st.markdown("---")
st.markdown("##### Variable reference")
st.caption("Full data dictionary is also available in docs/DATASET_SOURCE.md")
st.dataframe(
    {"column": df.columns.tolist(), "dtype": [str(t) for t in df.dtypes]},
    use_container_width=True,
)
