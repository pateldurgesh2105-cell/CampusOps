from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

P = Path(__file__).resolve().parents[1] / "data" / "processed"

INTENTS = {
    "building_complaints": ["which building has the most complaints", "building with highest complaints", "where are most complaints coming from"],
    "unresolved_department": ["which department has most unresolved complaints", "which department has pending issues", "where are unresolved complaints highest"],
    "energy": ["which building uses the most energy", "highest electricity consumption building", "where is energy usage highest"],
    "equipment": ["how many equipment items need repair", "which equipment is under maintenance", "equipment repair count"],
    "common_problem": ["what is the most common problem", "which complaint category is most common", "most frequent issue"],
}

_examples = [x for values in INTENTS.values() for x in values]
_labels = [label for label, values in INTENTS.items() for _ in values]
_vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
_matrix = _vectorizer.fit_transform(_examples)


def load_data():
    return (
        pd.read_csv(P / "complaints_clean.csv"),
        pd.read_csv(P / "energy_clean.csv"),
        pd.read_csv(P / "equipment_clean.csv"),
        pd.read_csv(P / "room_utilization_clean.csv"),
    )


def _intent(question):
    q = _vectorizer.transform([question.lower()])
    scores = cosine_similarity(q, _matrix)[0]
    best = scores.argmax()
    return _labels[best], float(scores[best])


def answer_question(question):
    c, e, equipment, _ = load_data()
    intent, confidence = _intent(question)
    if confidence < 0.22:
        return "I could not match that question to the available campus data."
    if intent == "building_complaints":
        s = c.groupby("building").size().sort_values(ascending=False)
        return f"{s.index[0]} has the highest number of recorded complaints with {int(s.iloc[0])} cases."
    if intent == "unresolved_department":
        s = c[c.status != "Resolved"].groupby("department").size().sort_values(ascending=False)
        return f"{s.index[0]} has the highest number of unresolved complaints with {int(s.iloc[0])} cases."
    if intent == "energy":
        s = e.groupby("building")["energy_kwh"].sum().sort_values(ascending=False)
        return f"{s.index[0]} has the highest recorded energy consumption at {s.iloc[0]:,.0f} kWh."
    if intent == "equipment":
        n = int(equipment.status.isin(["Needs Repair", "Under Maintenance"]).sum())
        return f"There are {n} equipment records marked for repair or maintenance."
    if intent == "common_problem":
        s = c.category.value_counts()
        return f"{s.index[0]} is the most common complaint category with {int(s.iloc[0])} recorded cases."
    return "I could not find a matching answer."
