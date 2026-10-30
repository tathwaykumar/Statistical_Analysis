"""Data ingestion for the UCI Student Performance dataset.

Source: UCI Machine Learning Repository, "Student Performance" dataset
(P. Cortez, A. Silva, 2008), https://archive.ics.uci.edu/dataset/320/student+performance
License: UCI permits academic/research re-use with attribution (CC BY 4.0 per
the UCI repository dataset card as of 2026).

Two raw files are provided by UCI: student-mat.csv (Math course, 395
students) and student-por.csv (Portuguese course, 649 students). Both share
an identical schema. We load each untouched, tag it with its subject, and
concatenate -- no values are altered, invented or dropped at this stage.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from config.student_config import DATA_RAW_DIR  # noqa: E402

MATH_FILE = DATA_RAW_DIR / "student-mat.csv"
POR_FILE = DATA_RAW_DIR / "student-por.csv"


def load_raw_subject(path: Path, subject: str) -> pd.DataFrame:
    """Load one raw UCI student-performance CSV, tagged with its subject."""
    df = pd.read_csv(path, sep=";")
    df.insert(0, "subject", subject)
    return df


OFFICIAL_UCI_MERGE_KEY = [
    "school", "sex", "age", "address", "famsize", "Pstatus", "Medu", "Fedu",
    "Mjob", "Fjob", "reason", "nursery", "internet",
]


def identify_subject_overlap(math_df: pd.DataFrame | None = None,
                              por_df: pd.DataFrame | None = None) -> dict:
    """Identify students present in both subject files.

    Uses the exact attribute key published by the dataset authors in their own
    merge script (student-merge.R) to find students who appear in both the
    Math and Portuguese files. The combined 1,044-row dataset therefore does
    NOT represent 1,044 unique students -- overlapping students contribute
    one row per subject. This matters for any analysis that treats the two
    subject samples as independent (see docs/DATASET_SOURCE.md).
    """
    if math_df is None:
        math_df = load_raw_subject(MATH_FILE, "Math")
    if por_df is None:
        por_df = load_raw_subject(POR_FILE, "Portuguese")

    overlap = math_df.merge(por_df, on=OFFICIAL_UCI_MERGE_KEY)
    n_overlap = len(overlap)
    n_math_only = len(math_df) - n_overlap
    n_por_only = len(por_df) - n_overlap
    return {
        "n_math_rows": len(math_df),
        "n_portuguese_rows": len(por_df),
        "n_overlapping_students": n_overlap,
        "n_math_only_students": n_math_only,
        "n_portuguese_only_students": n_por_only,
        "n_unique_students_estimate": n_overlap + n_math_only + n_por_only,
        "n_combined_rows": len(math_df) + len(por_df),
    }


def load_combined_raw() -> pd.DataFrame:
    """Load and concatenate both raw subject files, unmodified.

    Returns a single DataFrame with an added `subject` column
    ("Math" / "Portuguese") and a `student_id` row index. Students who take
    both subjects appear as two separate rows (one per subject) because the
    original dataset provides no persistent cross-file student identifier.
    """
    math_df = load_raw_subject(MATH_FILE, "Math")
    por_df = load_raw_subject(POR_FILE, "Portuguese")
    combined = pd.concat([math_df, por_df], ignore_index=True)
    combined.insert(0, "student_id", range(1, len(combined) + 1))
    return combined


if __name__ == "__main__":
    data = load_combined_raw()
    print(data.shape)
    print(data.head())
