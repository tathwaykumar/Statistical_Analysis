# Dataset Source

## Origin
- **Name:** Student Performance Data Set
- **Authors:** P. Cortez and A. Silva (2008)
- **Repository:** UCI Machine Learning Repository
- **URL:** https://archive.ics.uci.edu/dataset/320/student+performance
- **Citation:** Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School
  Student Performance.* In A. Brito and J. Teixeira (Eds.), Proceedings of 5th FUture BUsiness
  TEChnology Conference (FUBUTEC 2008), pp. 5-12.
- **License:** Released by UCI for academic/research re-use with attribution.
- **Original files used:** `student-mat.csv` (395 rows, Math course), `student-por.csv`
  (649 rows, Portuguese course), both bundled in `student.zip` inside the official UCI download.

## Why this dataset
Five candidate datasets were evaluated (UCI Student Performance, UCI Wine Quality, UCI Adult
Income, World Bank World Development Indicators subset, and a Kaggle retail sales dataset) against
the criteria in the project brief (authenticity, documentation quality, sample size, numeric and
categorical variable mix, missing-value profile, and fit for correlation/regression/hypothesis
testing/ANOVA). Student Performance scored highest: it has zero missing values by design, a
roughly even mix of 15 numeric and 17 categorical variables, an official, detailed data dictionary,
is of a suitable size (1,044 combined rows after merging both subject files), and its variables
map naturally onto every required statistical technique without forcing anything artificially.

## Preservation of raw data
The original, unmodified CSV files are kept at `data/raw/student-mat.csv` and
`data/raw/student-por.csv`. All cleaning happens in `src/data/clean.py`, which never deletes a row
except an exact full-record duplicate, and logs every step it takes.

## Combined dataset and verified student overlap
`src/data/ingest.py` concatenates both files and tags each row with a `subject` column
(`Math` / `Portuguese`), producing `data/processed/student_performance_clean.csv` (1,044 rows,
38 columns after derived-column enrichment).

**The 1,044 rows are NOT 1,044 unique students.** The dataset authors' own merge script
(`data/raw/student-merge.R`) identifies overlapping students by matching on 13 shared, course-
independent attributes (school, sex, age, address, famsize, Pstatus, Medu, Fedu, Mjob, Fjob,
reason, nursery, internet). `src/data/ingest.py::identify_subject_overlap()` reproduces this exact
key in Python and is run automatically during cleaning (`src/data/clean.py`). Verified result:

| Quantity | Value |
|---|---|
| Math rows | 395 |
| Portuguese rows | 649 |
| Overlapping students (in both files) | 382 |
| Math-only students | 13 |
| Portuguese-only students | 267 |
| **Estimated unique students** | **662** |
| Combined rows (what this project analyzes) | 1,044 |

Rows are intentionally **not deduplicated**: each row carries subject-specific grades (G1/G2/G3)
and potentially subject-specific behavioural answers (e.g. `studytime`, `paid`), so collapsing a
student's two subject rows into one would discard real information. The consequence is disclosed
explicitly wherever it matters: any statistical test that treats the two subject samples as
independent (notably the Math-vs-Portuguese variance F-test, research question RQ10) is in fact
comparing substantially overlapping groups, and its independence assumption should be read with
this caveat — see the Data Quality & Cleaning dashboard page, the PDF report's Limitations section,
and `tests/test_data_pipeline.py::test_subject_overlap_matches_official_merge_key`.

## Data Dictionary

| # | Variable | Type | Description |
|---|----------|------|--------------|
| - | student_id | int | Row identifier assigned during ingestion |
| - | subject | categorical | Course this record belongs to: Math or Portuguese |
| 1 | school | categorical (binary) | Student's school: GP or MS |
| 2 | sex | categorical (binary) | F or M |
| 3 | age | numeric | 15-22 |
| 4 | address | categorical (binary) | U (urban) or R (rural) |
| 5 | famsize | categorical (binary) | LE3 or GT3 |
| 6 | Pstatus | categorical (binary) | T (together) or A (apart) |
| 7 | Medu | numeric (ordinal) | Mother's education, 0-4 |
| 8 | Fedu | numeric (ordinal) | Father's education, 0-4 |
| 9 | Mjob | categorical (nominal) | teacher, health, services, at_home, other |
| 10 | Fjob | categorical (nominal) | teacher, health, services, at_home, other |
| 11 | reason | categorical (nominal) | home, reputation, course, other |
| 12 | guardian | categorical (nominal) | mother, father, other |
| 13 | traveltime | numeric (ordinal) | 1-4 |
| 14 | studytime | numeric (ordinal) | 1-4 |
| 15 | failures | numeric | past class failures, 0-4 |
| 16-23 | schoolsup, famsup, paid, activities, nursery, higher, internet, romantic | boolean | yes/no, converted to True/False |
| 24 | famrel | numeric (ordinal) | 1 (bad) - 5 (excellent) |
| 25 | freetime | numeric (ordinal) | 1-5 |
| 26 | goout | numeric (ordinal) | 1-5 |
| 27 | Dalc | numeric (ordinal) | workday alcohol consumption, 1-5 |
| 28 | Walc | numeric (ordinal) | weekend alcohol consumption, 1-5 |
| 29 | health | numeric (ordinal) | 1-5 |
| 30 | absences | numeric | 0-93 |
| 31 | G1 | numeric | first-period grade, 0-20 |
| 32 | G2 | numeric | second-period grade, 0-20 |
| 33 | G3 | numeric | final grade, 0-20 (primary outcome variable) |
| - | average_grade | derived numeric | mean(G1, G2, G3) |
| - | grade_trend | derived numeric | G3 - G1 |
| - | pass_fail | derived categorical | "Pass" if G3 >= 10 else "Fail" |

Full original documentation: `data/raw/student.txt`.
