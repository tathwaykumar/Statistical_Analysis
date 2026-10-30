"""Centralized student / project identity configuration.

Sensitive fields (registration number, faculty name) are loaded from
config/private.env, which is gitignored and kept out of version control.
Never commit real values for those fields.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CONFIG_DIR.parent

load_dotenv(CONFIG_DIR / "private.env")

STUDENT_NAME = "Tathwa Y Kumar"
UNIVERSITY = "Vellore Institute of Technology (VIT), Vellore"
PROGRAMME = "B.Tech Computer Science and Engineering"
SPECIALIZATION = "Data Science"
COURSE_NAME = "Probability and Statistics"
ACADEMIC_SEMESTER = "Fall Semester 2026"
ACADEMIC_YEAR = "2026-2027"

REGISTRATION_NUMBER = os.getenv("STUDENT_REGISTRATION_NUMBER", "[REGISTRATION_NUMBER_NOT_SET]")
FACULTY_NAME = os.getenv("FACULTY_NAME", "[FACULTY_NAME_NOT_SET]")
SCHOOL = os.getenv("SCHOOL_NAME", "School of Computer Science and Engineering (SCOPE)")

PROJECT_TITLE = "Statistical Data Analysis and Insights Platform"
PROJECT_SUBTITLE = (
    "A Comprehensive Statistical Investigation Using Probability, Correlation, "
    "Regression, Hypothesis Testing, ANOVA and Interactive Visualization"
)

DEFAULT_SIGNIFICANCE_LEVEL = 0.05

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
EXPORTS_DIR = OUTPUTS_DIR / "exports"
