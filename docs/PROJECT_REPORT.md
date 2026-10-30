# Project Report (Markdown companion to the PDF)

This file mirrors the structure and content of the generated PDF academic report
(`outputs/reports/Statistical_Data_Analysis_Report.pdf`) for quick reading without opening a PDF
viewer. The PDF is the authoritative, submission-ready version; both are generated from the same
code path (`src/report/pdf_report.py` and `src/report/findings.py`), so their numbers always
match.

## Title
Statistical Data Analysis and Insights Platform — A Comprehensive Statistical Investigation Using
Probability, Correlation, Regression, Hypothesis Testing, ANOVA and Interactive Visualization.

## Abstract
This report presents a statistical investigation of academic performance using the UCI Student
Performance dataset (Cortez & Silva, 2008), combining two real secondary-school cohorts
(Math, n=395; Portuguese, n=649; combined n=1,044). Descriptive statistics, probability analysis,
correlation, regression, hypothesis testing and ANOVA are applied to identify factors associated
with final grades. All results are computed directly from the dataset; no finding is hardcoded.

## Problem statement
Educational outcomes are influenced by a mix of demographic, behavioural and academic-history
factors. This project investigates which measurable variables are associated with secondary-school
final grades (G3), and whether demographic/behavioural subgroups differ meaningfully in
performance.

## Research objectives
See `docs/METHODOLOGY.md`.

## Dataset
See `docs/DATASET_SOURCE.md` for full source, license and data dictionary.

## Research questions, methods and results
Run `python -m src.report.findings` equivalent logic any time via the **Research Findings**
dashboard page, or regenerate the PDF (section "Results and Interpretation") — both pull from
`compute_all_findings()` in `src/report/findings.py`. As of the last generation run:

| ID | Question | Method |
|----|----------|--------|
| RQ1 | Distribution/normality of final grades | Descriptive stats + Shapiro-Wilk |
| RQ2 | Study time vs final grade | Pearson correlation |
| RQ3 | Absences vs final grade | Spearman correlation |
| RQ4 | Predicting G3 from G1/G2/studytime/absences | Multiple linear regression |
| RQ5 | Sex difference in G3 | Independent two-sample t-test |
| RQ6 | G1 vs G2 grade change | Paired t-test |
| RQ7 | Pass rate vs 60% benchmark | One-proportion z-test |
| RQ8 | Sex vs pass/fail independence | Chi-square test of independence |
| RQ9 | Mother's job vs G3 | One-way ANOVA + Tukey HSD |
| RQ10 | Math vs Portuguese grade variance | F-test for equal variances |
| RQ11 | Internet access vs pass likelihood | Conditional probability |

Exact numeric results are intentionally not hardcoded into this markdown file — view them live on
the **Research Findings** dashboard page or in the generated PDF, both always current.

## Discussion, limitations, conclusion, references
See the corresponding sections in the generated PDF — identical content, reproduced from the same
source. Key points: prior grades (G1, G2) dominate as predictors of G3; study time has a weak but
significant positive association; the dataset's self-report and single-era/two-school scope limit
generalizability; all correlational/regression findings are explicitly framed as association, not
causation.
