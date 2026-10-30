import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_alpha, get_data, identity_footer, page_header  # noqa: E402
from src.stats import anova  # noqa: E402
from src.visualization.plots import bar_group_means, box_plot  # noqa: E402

st.set_page_config(page_title="ANOVA", layout="wide")
page_header("Analysis of Variance (ANOVA)")
identity_footer()

df, _ = get_data()
alpha = get_alpha()

st.markdown("##### One-way ANOVA")
value_col = st.selectbox("Dependent variable", ["G3", "G1", "G2", "average_grade", "absences"])
group_col = st.selectbox("Grouping factor", ["Mjob", "Fjob", "reason", "guardian", "studytime", "traveltime"])

result = anova.one_way_anova(df, value_col, group_col, alpha=alpha)

c1, c2, c3, c4 = st.columns(4)
c1.metric("F-statistic", f"{result['f_statistic']:.3f}")
c2.metric("p-value", f"{result['p_value']:.4g}")
c3.metric("F-critical", f"{result['f_critical']:.3f}")
c4.metric("eta-squared", f"{result['eta_squared']:.3f}")

st.markdown("##### ANOVA summary table")
st.dataframe({
    "Source": ["Between groups", "Within groups", "Total"],
    "SS": [result["ssb"], result["ssw"], result["sst"]],
    "df": [result["df_between"], result["df_within"], result["df_between"] + result["df_within"]],
    "MS": [result["msb"], result["msw"], None],
    "F": [result["f_statistic"], None, None],
}, use_container_width=True)

st.markdown("##### Mandatory mathematical validation")
c1, c2 = st.columns(2)
if result["decomposition_valid"]:
    c1.success("SST = SSB + SSW verified ✓")
else:
    c1.error("Decomposition check FAILED")
if result["f_cross_check_valid"]:
    c2.success("F-statistic cross-check verified ✓")
else:
    c2.error("F cross-check FAILED")
st.caption(f"SST = {result['sst']:.3f}  =  SSB ({result['ssb']:.3f}) + SSW ({result['ssw']:.3f}) "
           f"= {result['ssb'] + result['ssw']:.3f}")

st.markdown("##### Assumption check: homogeneity of variance (Levene's test)")
st.write(f"Levene statistic = {result['levene_statistic']:.3f}, p = {result['levene_p_value']:.4g} -> "
         f"{'assumption holds' if result['variance_homogeneity_ok_at_0.05'] else 'assumption violated'} at 0.05")

if not result["variance_homogeneity_ok_at_0.05"]:
    welch = anova.welch_anova(df, value_col, group_col, alpha=alpha)
    st.warning("Variance homogeneity violated — Welch's ANOVA (variance-robust alternative) reported below.")
    st.json(welch)

c1, c2 = st.columns(2)
c1.plotly_chart(box_plot(df, value_col, group_col), use_container_width=True, theme=None)
c2.plotly_chart(bar_group_means(result["group_stats"], f"Mean {value_col} by {group_col}"), use_container_width=True, theme=None)

if result["tukey_posthoc"] is not None:
    st.markdown("##### Tukey HSD post-hoc comparisons")
    st.dataframe(result["tukey_posthoc"], use_container_width=True)

decision = "Reject H0 (at least one group mean differs)" if result["reject_h0"] else "Fail to reject H0"
st.info(f"**Decision at alpha={alpha}:** {decision}. eta-squared = {result['eta_squared']:.3f} "
        f"(proportion of variance in {value_col} explained by {group_col}).")
