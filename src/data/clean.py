"""Data cleaning and validation for the combined student-performance dataset.

Design principle: never silently drop or alter observations. Every decision
made here is recorded in a cleaning log returned alongside the cleaned
DataFrame, so the dashboard and report can display exactly what was done.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.data.ingest import identify_subject_overlap, load_combined_raw  # noqa: E402

NUMERIC_COLUMNS = [
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health", "absences",
    "G1", "G2", "G3",
]
CATEGORICAL_COLUMNS = [
    "school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
    "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
    "nursery", "higher", "internet", "romantic", "subject",
]
BINARY_YN_COLUMNS = [
    "schoolsup", "famsup", "paid", "activities", "nursery", "higher",
    "internet", "romantic",
]


@dataclass
class CleaningReport:
    steps: list[str] = field(default_factory=list)
    duplicates_found: int = 0
    duplicates_dropped: int = 0
    missing_before: dict = field(default_factory=dict)
    missing_after: dict = field(default_factory=dict)
    outliers: dict = field(default_factory=dict)
    rows_before: int = 0
    rows_after: int = 0
    subject_overlap: dict = field(default_factory=dict)

    def log(self, message: str) -> None:
        self.steps.append(message)


def detect_outliers_iqr(series: pd.Series) -> pd.Series:
    """Boolean mask of IQR-rule outliers (outside Q1 - 1.5*IQR, Q3 + 1.5*IQR)."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return (series < lower) | (series > upper)


def clean_dataset(raw: pd.DataFrame | None = None) -> tuple[pd.DataFrame, CleaningReport]:
    """Validate and lightly enrich the raw dataset.

    No row is dropped unless it is an exact full-row duplicate (same student
    record repeated verbatim), since the source dataset documents no missing
    values by design. Outliers are flagged, not removed -- they are
    legitimate extreme observations (e.g. high absence counts) and removing
    them would bias inference.
    """
    df = raw.copy() if raw is not None else load_combined_raw()
    report = CleaningReport(rows_before=len(df))

    report.missing_before = df.isna().sum().to_dict()
    report.log(f"Loaded {len(df)} rows x {df.shape[1]} columns from raw UCI CSV files.")

    report.subject_overlap = identify_subject_overlap()
    ov = report.subject_overlap
    report.log(
        f"Subject-overlap check (using the dataset authors' own merge key from student-merge.R): "
        f"{ov['n_overlapping_students']} of {ov['n_math_rows']} Math students also appear in the "
        f"Portuguese file. The combined {ov['n_combined_rows']}-row dataset therefore represents "
        f"only ~{ov['n_unique_students_estimate']} unique students, not {ov['n_combined_rows']}. "
        f"Rows are kept per-subject (not deduplicated) because each row reflects subject-specific "
        f"grades (G1/G2/G3) and some subject-specific fields (e.g. paid, studytime may differ by "
        f"course); this is disclosed as a limitation for any analysis that assumes independent rows."
    )

    dup_mask = df.drop(columns=["student_id"]).duplicated()
    report.duplicates_found = int(dup_mask.sum())
    if report.duplicates_found:
        df = df[~dup_mask].reset_index(drop=True)
        df["student_id"] = range(1, len(df) + 1)
        report.duplicates_dropped = report.duplicates_found
        report.log(f"Dropped {report.duplicates_dropped} exact-duplicate rows.")
    else:
        report.log("No exact-duplicate rows found; none dropped.")

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="raise")

    for col in NUMERIC_COLUMNS:
        mask = detect_outliers_iqr(df[col])
        if mask.any():
            report.outliers[col] = int(mask.sum())
    report.log(
        f"Flagged (not removed) IQR-rule outliers in {len(report.outliers)} numeric "
        f"columns: {report.outliers}"
    )

    for col in BINARY_YN_COLUMNS:
        df[col] = df[col].map({"yes": True, "no": False})

    df["average_grade"] = df[["G1", "G2", "G3"]].mean(axis=1).round(2)
    df["grade_trend"] = (df["G3"] - df["G1"]).round(2)
    df["pass_fail"] = np.where(df["G3"] >= 10, "Pass", "Fail")
    report.log(
        "Derived columns added: average_grade (mean of G1/G2/G3), "
        "grade_trend (G3 - G1), pass_fail (G3 >= 10 -> Pass, VIT/UCI-standard "
        "20-point passing threshold used by the dataset authors)."
    )

    report.missing_after = df.isna().sum().to_dict()
    report.rows_after = len(df)
    return df, report


def save_processed(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)


if __name__ == "__main__":
    from config.student_config import DATA_PROCESSED_DIR

    cleaned, rep = clean_dataset()
    save_processed(cleaned, DATA_PROCESSED_DIR / "student_performance_clean.csv")
    for step in rep.steps:
        print("-", step)
    print("Final shape:", cleaned.shape)
