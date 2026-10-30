import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.common import get_alpha, get_data, identity_footer, page_header  # noqa: E402
from src.stats import hypothesis  # noqa: E402

st.set_page_config(page_title="Hypothesis Testing", layout="wide")
page_header("Hypothesis Testing")
identity_footer()

df, _ = get_data()
alpha = get_alpha()

test_choice = st.selectbox("Select a test", [
    "One-sample t-test: Is mean G3 different from 10 (pass mark)?",
    "Independent two-sample t-test: G3 by sex",
    "Paired t-test: G1 vs G2 (grade improvement)",
    "Proportion z-test: Pass rate vs 60% benchmark",
    "Chi-square test of independence: sex vs pass_fail",
    "Chi-square goodness-of-fit: Mjob category distribution",
    "F-test for equal variances: G3 variance, Math vs Portuguese",
])

st.markdown(f"**Significance level (alpha): {alpha}**")


def render(result):
    s = result.summary()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test statistic", f"{s['test_statistic']:.4f}")
    c2.metric("p-value", f"{s['p_value']:.4g}")
    c3.metric("Critical value", f"{s['critical_value']:.4f}" if s["critical_value"] is not None else "n/a")
    c4.metric("Decision", s["decision"])
    st.write(f"**H0:** {s['h0']}  |  **H1:** {s['h1']}")
    st.write(f"**Degrees of freedom:** {s['degrees_of_freedom']}")
    if s["confidence_interval"]:
        st.write(f"**95% CI:** [{s['confidence_interval'][0]:.4f}, {s['confidence_interval'][1]:.4f}]")
    st.write("**Assumptions checked:**")
    for a in s["assumptions"]:
        st.markdown(f"- {a}")
    is_sig = s["p_value"] < alpha
    verdict = "statistically significant" if is_sig else "not statistically significant"
    message = f"At alpha = {alpha}, the result is **{verdict}** (p = {s['p_value']:.4g})."
    if is_sig:
        st.success(message)
    else:
        st.info(message)
    if s["extra"]:
        with st.expander("Additional detail"):
            st.json({k: v for k, v in s["extra"].items() if k != "contingency_table"})


if test_choice.startswith("One-sample"):
    res = hypothesis.one_sample_ttest(df["G3"], 10, alpha=alpha,
                                       question="Is the mean final grade (G3) different from the pass mark of 10?")
    render(res)
elif test_choice.startswith("Independent"):
    res = hypothesis.two_sample_ttest(df[df.sex == "M"]["G3"], df[df.sex == "F"]["G3"], alpha=alpha,
                                       question="Do male and female students differ in final grade (G3)?")
    render(res)
elif test_choice.startswith("Paired"):
    res = hypothesis.paired_ttest(df["G1"], df["G2"], alpha=alpha,
                                   question="Does the second-period grade (G2) differ significantly from the first (G1)?")
    render(res)
elif test_choice.startswith("Proportion"):
    successes = int((df["pass_fail"] == "Pass").sum())
    res = hypothesis.proportion_ztest(successes, len(df), 0.60, alpha=alpha,
                                       question="Does the actual pass rate differ from an assumed 60% benchmark?")
    render(res)
elif test_choice.startswith("Chi-square test of independence"):
    res = hypothesis.chi_square_independence(df, "sex", "pass_fail", alpha=alpha,
                                              question="Is passing (G3>=10) independent of student sex?")
    render(res)
elif test_choice.startswith("Chi-square goodness-of-fit"):
    observed = df["Mjob"].value_counts().sort_index()
    res = hypothesis.chi_square_goodness_of_fit(observed.to_numpy(), alpha=alpha,
                                                 question="Is mother's job category uniformly distributed?")
    render(res)
else:
    res = hypothesis.f_test_variances(df[df.subject == "Math"]["G3"], df[df.subject == "Portuguese"]["G3"],
                                       alpha=alpha,
                                       question="Do Math and Portuguese final grades have equal variance?")
    render(res)
    st.warning(
        "Independence caveat: 382 of the 395 Math students also appear in the Portuguese sample "
        "(verified via the dataset authors' own merge key in student-merge.R), so these two "
        "groups substantially overlap rather than being independent. This test's 'independent "
        "samples' assumption is violated — see the Data Quality & Cleaning page for details."
    )
