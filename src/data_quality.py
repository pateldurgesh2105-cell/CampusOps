from pathlib import Path
import pandas as pd

P = Path(__file__).resolve().parents[1] / "data/processed"


def run_checks():
    c = pd.read_csv(P / "complaints_clean.csv")
    e = pd.read_csv(P / "energy_clean.csv")
    q = pd.read_csv(P / "equipment_clean.csv")
    return {
        "complaint_id_unique": c["complaint_id"].is_unique,
        "complaint_dates_valid": c["created_date"].notna().all(),
        "energy_non_negative": (e["energy_kwh"] >= 0).all(),
        "equipment_id_unique": q["equipment_id"].is_unique,
    }


if __name__ == "__main__":
    for k, v in run_checks().items():
        print(k, "PASS" if v else "FAIL")
