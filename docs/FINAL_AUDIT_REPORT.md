# Final Independent Academic and Statistical Audit

> **Addendum (same day):** a follow-up visual/UX/functional audit using the Playwright MCP
> server found and fixed a theme-override bug causing unreadable chart legends in dark-mode
> browsers, plus two real functional defects (a debug-text leak on the ANOVA page and a
> malformed p-value in the Regression coefficients table). See
> "Visual/UX/Functional Audit Addendum" at the end of this document. The statistical findings
> and corrections below are unaffected and remain accurate.

Date: 2026-10-30
Auditor: Claude Sonnet 5, acting as an independent reviewer of the already-built project
(same codebase, deliberately re-verified from scratch rather than trusted at face value).

## Audit methodology
For each statistical module, calculations were re-derived using a code path independent of the
project's own wrapper functions (direct `scipy.stats`, direct `statsmodels.api.OLS`, and
hand-written manual formulas from raw group data), then compared numerically
(`numpy.isclose`) against the project's reported values. The dataset merge was re-examined against
the dataset authors' own merge script rather than trusting the project's prior description. All
13 dashboard pages were executed headlessly via `streamlit.testing.v1.AppTest` (not just HTTP-200
checked), including simulated widget interactions. The full pytest suite was run before and after
fixes. Documentation and the PDF report were checked line-by-line against the live findings
module for numeric consistency, and all literature citations were checked for real-world existence
and correct publication details.

## Issues discovered

### 1. Dataset merge overlap was understated (material finding)
The project previously described the 1,044-row combined dataset only as "395 Math + 649
Portuguese rows," with a limitations note that some of the ~382 students appearing in both files
were "treated as independent" due to lacking a persistent ID. On independent inspection of
`data/raw/student-merge.R` (the dataset authors' own merge script), I confirmed this is not merely
an approximate caveat — it is exactly reproducible: using the authors' 13-attribute merge key
(school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob, reason, nursery, internet),
**382 of the 395 Math students (96.7%) also appear in the Portuguese file**. The combined dataset
of 1,044 rows therefore represents only an estimated **662 unique students**, not 1,044.

This directly affects **RQ10** (F-test comparing Math vs. Portuguese G3 variance): the two
"independent" samples share 382 of the same students, so the test's independence assumption is
violated in a way that was previously only vaguely gestured at, not quantified or flagged where
the result itself is shown.

**Severity:** Medium — the computation itself (the F-statistic, p-value) is numerically correct;
the issue is that the test's applicability/interpretation was not clearly flagged next to the
result, risking a reader taking RQ10's "Reject H0" at face value as two independent cohorts
differing in variance.

### 2. Minor: no git repository yet, so "exclude from tracking" was not literally testable
Point 13 of the audit brief asks to confirm `config/private.env` and registration information are
excluded from Git tracking. No `.git` directory exists in this project yet (confirmed via
`git status` → "not a git repository"), so there is nothing currently tracked, trackable, or
untracked to check. `.gitignore` already lists `config/private.env` preemptively, so the first
`git init` + `git add` in this directory will correctly exclude it. This is not a defect, just a
precondition noted for completeness.

### 3. No fabricated approvals, results, or citations found
- Faculty name, registration number, and student details are real user-supplied values stored in
  the gitignored `config/private.env`, not fabricated.
- No claim of faculty approval, university endorsement, or academic-credit approval exists
  anywhere in the dashboard, PDF, or docs (explicitly disclaimed in `app/pages/12_About.py` and
  the PDF cover material).
- Citations checked: Cortez & Silva (2008) FUBUTEC paper matches the UCI dataset page's own
  citation. Montgomery, *Design and Analysis of Experiments* (9th ed., Wiley) and Field,
  *Discovering Statistics Using IBM SPSS Statistics* (5th ed., Sage, 2017) are real, correctly
  attributed textbooks used as general methodological references (not pinpoint-quoted) — this is
  disclosed here for transparency since they support general statistical practice rather than a
  specific number in the report.

## Corrections made
1. Added `identify_subject_overlap()` to `src/data/ingest.py`, reproducing the dataset authors'
   exact merge key from `student-merge.R` in Python, returning verified overlap counts.
2. Wired this into `CleaningReport` (`src/data/clean.py`) as `subject_overlap`, logged automatically
   on every cleaning run.
3. Added a dedicated "Student overlap between subject files" section to the **Data Quality &
   Cleaning** dashboard page, showing the 382/13/267/662 figures and an explicit warning about the
   independence violation.
4. Added a live warning directly under the F-test result on the **Hypothesis Testing** page when
   the Math-vs-Portuguese variance test is selected.
5. Updated `src/report/findings.py` (RQ10) and `src/report/pdf_report.py` (Limitations section) so
   the PDF report states the same verified numbers and caveat — the dashboard and PDF remain
   numerically identical, now including this disclosure.
6. Rewrote `docs/DATASET_SOURCE.md`'s dataset-merge section with the exact verified table
   (395 / 649 / 382 / 13 / 267 / 662 / 1,044) instead of the previous approximate wording.
7. Added two new regression tests (`tests/test_data_pipeline.py`):
   `test_subject_overlap_matches_official_merge_key` (locks the verified 382/662 figures against
   drift) and `test_cleaning_report_includes_subject_overlap`.

No other genuine defects were found; no redesign or new features were introduced beyond what was
needed to surface and correct this finding.

## Statistical verification results
All re-derivations matched the project's own reported values to floating-point precision
(`numpy.isclose`):

| Check | Independent method | Result |
|---|---|---|
| Regression R², coefficients, F-statistic | Direct `statsmodels.OLS` on the same design matrix | Match |
| Manual R² from residual/total sum of squares | Hand-computed from residuals | Match (0.8337229...) |
| Two-sample t-test (sex vs. G3) | Direct `scipy.stats.ttest_ind` | Match (statistic and p-value) |
| Chi-square independence (sex vs. pass/fail) | Direct `scipy.stats.chi2_contingency` | Match (statistic, df, p-value) |
| ANOVA SSB, SSW, SST (Mjob vs. G3) | Hand-computed from raw group means, independent of the project's own function | Match; **SST = SSB + SSW confirmed** (15,578.92 = 459.03 + 15,119.89) |
| ANOVA F-statistic | Direct `scipy.stats.f_oneway` | Match |
| Tukey HSD post-hoc | Present and computed via `statsmodels.stats.multicomp.pairwise_tukeyhsd` when omnibus test is significant | Present, correctly gated |
| Pearson correlation and 95% CI | Direct `scipy.stats.pearsonr`; CI contains point estimate | Match |
| Student-overlap count | Dataset authors' own `student-merge.R` key, reproduced in Python | 382 overlapping students confirmed exactly |

Full automated suite: **24/24 tests passed** (`pytest tests/ -q`), including the 2 new overlap
regression tests added during this audit. All 13 dashboard pages pass headless execution with
zero exceptions (`streamlit.testing.v1.AppTest`), both at default state and after simulated widget
interaction (verified explicitly for the Hypothesis Testing page's test-selector dropdown).

PDF-vs-dashboard-vs-findings-module consistency: confirmed structurally, since both the dashboard's
Research Findings page and the PDF report call the identical `compute_all_findings()` function on
the identical cleaned DataFrame — there is no separate "PDF-only" calculation path that could
drift from the dashboard. The regenerated PDF (12 pages) was confirmed to contain the new overlap
figures ("382" verified present in extracted PDF text).

## Remaining limitations (disclosed, not defects)
- The dataset is self-reported survey + school-record data from two Portuguese secondary schools
  in 2008; findings do not generalize beyond that population/era.
- RQ10's independence violation is now disclosed everywhere the result appears, but the test
  itself is still reported (not removed) since it remains a legitimate illustration of the F-test
  mechanics in this project's academic scope; readers are told explicitly to interpret it with
  caution rather than as a clean two-cohort comparison.
- Generic textbook references (Montgomery, Field) support general methodology, not specific
  reported numbers — this is now explicitly noted above rather than left ambiguous.
- No git repository exists yet in this directory; the private.env exclusion is correctly
  pre-configured in `.gitignore` but has not yet been exercised by an actual `git init`/commit.

## Final readiness assessment
**Ready for academic demonstration and viva**, with one material correction applied: the
Math/Portuguese student overlap is now independently verified, quantified (382 overlapping / 662
unique students), and disclosed consistently across the dataset documentation, the Data Quality
dashboard page, the Hypothesis Testing page, the PDF report, and a new regression test that
prevents this figure from silently drifting if the raw data source changes. All other statistical
computations (descriptive statistics, probability, correlation, regression, hypothesis testing,
ANOVA including the mandatory SST = SSB + SSW decomposition) were independently re-verified and
found correct. No fabricated data, results, approvals, or citations were found anywhere in the
project.

---

## Visual/UX/Functional Audit Addendum

Tooling: Microsoft's official Playwright MCP server (`@playwright/mcp`), registered via a
project-scoped `.mcp.json` and connected for this session. All 13 dashboard pages were opened in
a real Chromium browser, inspected via accessibility snapshots and screenshots, and tested under
both standard (light) and emulated `prefers-color-scheme: dark` conditions.

### Root cause of the reported "white on white" legends/text
`st.plotly_chart()` applies Streamlit's own auto-theming to a figure's colours by default,
overriding whatever colours the figure itself sets, to match the *viewer's* ambient
browser/OS colour scheme. The project had no `.streamlit/config.toml` pinning a theme, and no
`st.plotly_chart()` call passed `theme=None`. So on a dark-mode browser/OS, Streamlit silently
recoloured every chart's background/text to dark-theme values regardless of the explicit
navy/white/charcoal palette set in `src/visualization/plots.py`, producing low-contrast or
white-on-white legends, axis labels and titles exactly as reported — confirmed reproduced in this
audit with `browser_emulate_media(colorScheme: dark)` before the fix, and confirmed resolved
after.

### Fixes applied
1. `.streamlit/config.toml` — pinned `base = "light"` with the project's own navy/accent-blue/
   charcoal palette, so the app always renders the same regardless of the viewer's OS/browser
   theme preference.
2. Added `theme=None` to all 15 `st.plotly_chart()` calls across `app/pages/*.py` so Streamlit no
   longer overrides the figures' explicit colours.
3. `src/visualization/plots.py` — added `style_figure()` and strengthened `_base_layout()` with
   explicit legend/axis colours (white background, charcoal text, light grid lines) so every chart
   in the app, including ad-hoc ones, shares one consistent, theme-proof visual system.
4. `app/pages/9_Interactive_Visualizations.py` — the five charts on this page previously used raw,
   unstyled `plotly.express` calls; now routed through `style_figure()` for visual consistency with
   the rest of the app (titles, axis labels, legend box added where missing).

### Two real functional bugs found and fixed while testing
1. **`app/pages/8_ANOVA.py`** — two bare ternary statements
   (`c1.success(...) if ... else c1.error(...)`) were, as top-level expressions, caught by
   Streamlit's "magic" auto-display and rendered as raw Python source plus a `DeltaGenerator`
   object repr directly on the page, visible to any user viewing the ANOVA page. Rewritten as
   explicit `if/else` statements. (Same bug class as an earlier fix on the Hypothesis Testing
   page from the prior development session — grepped the rest of the codebase afterward; no other
   instances found.)
2. **`app/pages/6_Regression_Analysis.py`** — the coefficients table passed raw floats straight
   into `st.dataframe()`; for G2's p-value (~1.87×10⁻¹⁶⁶), Streamlit's automatic numeric
   formatting expanded it to roughly 170 literal zeros, breaking the table's layout. Fixed by
   formatting all numeric columns (coefficient, std_error, p_value, VIF) as strings with
   appropriate precision/scientific notation before display.

### Re-verification after fixes
- Full pytest suite: 24/24 passing.
- Headless `streamlit.testing.v1.AppTest` sweep of all 13 pages: zero exceptions.
- All 13 pages re-visited in the browser (light mode and simulated dark mode); charts, legends,
  tables and metric cards confirmed readable in both.
- PDF report regenerated through the actual "Generate PDF report" dashboard button (not just the
  CLI): 12 pages, contains the verified "382" overlap figure, "Rachna Bhatia", and "25BDS0209".
- The 382-student overlap figure and the independence-violation caveat text (dataset docs, Data
  Quality page, Hypothesis Testing F-test warning, PDF Limitations) were confirmed unchanged and
  intact throughout — no statistical finding, dataset value, or citation was altered by this pass,
  only presentation/formatting code.
- No fabricated faculty endorsement, approval, or designation was introduced; "Rachna Bhatia" is
  shown without an invented title, consistent with what was actually supplied.

### Remaining observations (not defects)
- Streamlit logs benign `_stcore/health` / `_stcore/host-config` 404s in the browser console when
  a page is opened by direct URL navigation (as Playwright testing does) rather than via in-app
  sidebar clicks; this is a Streamlit framework artifact of direct deep-linking, not an
  application bug, and does not affect normal user navigation.
- Two-way ANOVA remains implemented but without a dedicated dashboard page (pre-existing, noted in
  `docs/PROGRESS_CHECKLIST.md`).
