import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from data_pipeline import ensure_data, clean_complaints
from data_quality import run_checks


def test_cleaning_reduces_duplicates():
    ensure_data()
    r = clean_complaints()
    assert r["duplicates_removed"] > 0
    assert r["rows_after"] < r["rows_before"]


def test_quality():
    ensure_data()
    clean_complaints()
    assert all(run_checks().values())
