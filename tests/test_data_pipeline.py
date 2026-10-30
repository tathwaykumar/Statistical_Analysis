import numpy as np
import pandas as pd
import pytest

from src.data.clean import clean_dataset
from src.data.ingest import identify_subject_overlap, load_combined_raw


@pytest.fixture(scope="module")
def raw():
    return load_combined_raw()


@pytest.fixture(scope="module")
def cleaned():
    df, report = clean_dataset()
    return df, report


def test_raw_shape(raw):
    assert raw.shape[0] == 395 + 649
    assert "subject" in raw.columns
    assert set(raw["subject"].unique()) == {"Math", "Portuguese"}


def test_cleaning_preserves_row_count_when_no_duplicates(cleaned):
    df, report = cleaned
    assert len(df) == report.rows_after
    assert report.rows_before == 1044


def test_no_missing_values_after_cleaning(cleaned):
    df, _ = cleaned
    assert df.isna().sum().sum() == 0


def test_derived_columns_present(cleaned):
    df, _ = cleaned
    for col in ["average_grade", "grade_trend", "pass_fail"]:
        assert col in df.columns
    assert set(df["pass_fail"].unique()) <= {"Pass", "Fail"}


def test_average_grade_matches_manual_mean(cleaned):
    df, _ = cleaned
    manual = df[["G1", "G2", "G3"]].mean(axis=1).round(2)
    assert np.allclose(df["average_grade"], manual)


def test_pass_fail_consistent_with_threshold(cleaned):
    df, _ = cleaned
    assert ((df["G3"] >= 10) == (df["pass_fail"] == "Pass")).all()


def test_subject_overlap_matches_official_merge_key():
    """The 1,044 combined rows are not 1,044 unique students -- 382 overlap per the
    dataset authors' own student-merge.R key. This is a documented limitation, not a bug,
    but must stay correct: if this number ever drifts, downstream docs/PDF claims go stale."""
    overlap = identify_subject_overlap()
    assert overlap["n_math_rows"] == 395
    assert overlap["n_portuguese_rows"] == 649
    assert overlap["n_overlapping_students"] == 382
    assert overlap["n_math_only_students"] == 13
    assert overlap["n_portuguese_only_students"] == 267
    assert overlap["n_unique_students_estimate"] == 662
    assert overlap["n_combined_rows"] == 1044


def test_cleaning_report_includes_subject_overlap(cleaned):
    _, report = cleaned
    assert report.subject_overlap["n_overlapping_students"] == 382
