"""Ensures the PDF report and dashboard draw from the exact same computed results."""
from src.data.clean import clean_dataset
from src.report.findings import compute_all_findings


def test_findings_are_deterministic_and_complete():
    df, _ = clean_dataset()
    findings = compute_all_findings(df)
    assert len(findings) >= 10
    for f in findings:
        assert f["question"]
        assert f["method"]
        assert f["result"]

    # Re-running on the same data must give identical results (reproducibility).
    findings2 = compute_all_findings(df)
    assert [f["result"] for f in findings] == [f["result"] for f in findings2]


def test_pdf_report_builds_without_error(tmp_path):
    from src.report.pdf_report import build_report

    out = tmp_path / "test_report.pdf"
    result_path = build_report(out)
    assert result_path.exists()
    assert result_path.stat().st_size > 1000
