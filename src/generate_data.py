from pathlib import Path
import random
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"

random.seed(42)

BUILDINGS = ["Admin Block", "Engineering Block", "Science Block", "Library", "Hostel"]
CATEGORIES = ["Electrical", "Plumbing", "IT", "Furniture", "Cleaning", "HVAC"]
DEPARTMENTS = ["Maintenance", "IT Support", "Housekeeping", "Electrical"]
STATUSES = ["Resolved", "Pending", "In Progress"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]
PROBLEMS = {
    "Electrical": "power fluctuation in room",
    "Plumbing": "water leakage near washroom",
    "IT": "network connection is unstable",
    "Furniture": "damaged chair or desk",
    "Cleaning": "cleaning required in common area",
    "HVAC": "air conditioner not cooling properly",
}


def generate():
    RAW.mkdir(parents=True, exist_ok=True)

    complaints = []
    for i in range(1, 1201):
        category = random.choice(CATEGORIES)
        complaints.append({
            "complaint_id": f"CMP{i:05d}",
            "created_date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=random.randint(0, 242)),
            "building": random.choice(BUILDINGS),
            "room_no": random.randint(101, 520),
            "category": category,
            "description": PROBLEMS[category],
            "department": random.choice(DEPARTMENTS),
            "priority": random.choices(PRIORITIES, weights=[35, 40, 20, 5])[0],
            "status": random.choices(STATUSES, weights=[60, 20, 20])[0],
            "resolution_days": random.randint(1, 12),
        })
    df = pd.DataFrame(complaints)
    df = pd.concat([df, df.iloc[[10, 25, 50]].copy()], ignore_index=True)
    df.to_csv(RAW / "complaints.csv", index=False)

    dates = pd.date_range("2026-01-01", "2026-08-31", freq="D")
    energy = pd.DataFrame([
        {"date": d, "building": b, "energy_kwh": random.randint(250, 950)}
        for d in dates for b in BUILDINGS
    ])
    energy.to_csv(RAW / "energy_usage.csv", index=False)

    equipment = pd.DataFrame([
        {
            "equipment_id": f"EQ{i:04d}",
            "building": random.choice(BUILDINGS),
            "equipment_type": random.choice(["Projector", "AC", "Desktop", "Printer", "UPS"]),
            "brand": random.choice(["Dell", "HP", "LG", "Epson", "Voltas"]),
            "status": random.choice(["Working", "Working", "Needs Repair", "Under Maintenance"]),
            "installed_date": pd.Timestamp("2023-01-01") + pd.Timedelta(days=random.randint(0, 900)),
        }
        for i in range(1, 181)
    ])
    equipment.to_csv(RAW / "equipment.csv", index=False)

    rooms = pd.DataFrame([
        {
            "room_no": i,
            "building": random.choice(BUILDINGS),
            "room_type": random.choice(["Classroom", "Lab", "Seminar Hall"]),
            "avg_utilization_pct": random.randint(25, 98),
        }
        for i in range(101, 161)
    ])
    rooms.to_csv(RAW / "room_utilization.csv", index=False)
    print("Synthetic CampusOps data generated.")


if __name__ == "__main__":
    generate()
