from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "data/processed"


def ensure_data():
    """Create the demo dataset and processed files when needed."""
    required = [
        RAW / "complaints.csv",
        RAW / "energy_usage.csv",
        RAW / "equipment.csv",
        RAW / "room_utilization.csv",
    ]
    if not all(p.exists() for p in required):
        from generate_data import generate
        generate()
    if not (OUT / "complaints_clean.csv").exists():
        process_all()


def clean_complaints():
    df = pd.read_csv(RAW / "complaints.csv")
    before = len(df)
    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df = df.dropna(subset=["complaint_id", "created_date", "category", "status"])
    df = df.drop_duplicates(
        subset=["building", "room_no", "category", "description", "department"],
        keep="first",
    )
    df["resolution_days"] = pd.to_numeric(df["resolution_days"], errors="coerce")
    df["priority_score"] = df["priority"].map(
        {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    )
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "complaints_clean.csv", index=False)
    return {"rows_before": before, "rows_after": len(df), "duplicates_removed": before - len(df)}


def process_energy():
    df = pd.read_csv(RAW / "energy_usage.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["energy_kwh"] = pd.to_numeric(df["energy_kwh"], errors="coerce")
    df.dropna().to_csv(OUT / "energy_clean.csv", index=False)


def process_equipment():
    pd.read_csv(RAW / "equipment.csv").drop_duplicates("equipment_id").to_csv(
        OUT / "equipment_clean.csv", index=False
    )


def process_rooms():
    df = pd.read_csv(RAW / "room_utilization.csv")
    df["avg_utilization_pct"] = pd.to_numeric(df["avg_utilization_pct"], errors="coerce")
    df.dropna().to_csv(OUT / "room_utilization_clean.csv", index=False)


def process_all():
    print(clean_complaints())
    process_energy()
    process_equipment()
    process_rooms()
    print("Processing completed.")


if __name__ == "__main__":
    ensure_data()
    process_all()
