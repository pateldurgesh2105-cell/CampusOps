from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))
from data_pipeline import ensure_data
from insights import load_data, answer_question

ensure_data()
st.set_page_config(page_title="CampusOps", page_icon="🏫", layout="wide")
complaints, energy, equipment, rooms = load_data()

st.title("CampusOps")
st.caption("College Operations Intelligence")

with st.sidebar:
    st.header("Filters")
    selected_buildings = st.multiselect("Building", sorted(complaints.building.unique()))
    selected_status = st.multiselect("Status", sorted(complaints.status.unique()))

filtered = complaints.copy()
if selected_buildings:
    filtered = filtered[filtered.building.isin(selected_buildings)]
if selected_status:
    filtered = filtered[filtered.status.isin(selected_status)]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Complaints", f"{len(filtered):,}")
c2.metric("Unresolved", f"{(filtered.status != 'Resolved').sum():,}")
c3.metric("High / Critical", f"{filtered.priority.isin(['High', 'Critical']).sum():,}")
c4.metric("Avg Resolution (days)", f"{filtered.resolution_days.mean():.1f}")

left, right = st.columns(2)
with left:
    x = filtered.category.value_counts().reset_index()
    x.columns = ["category", "count"]
    st.plotly_chart(px.bar(x, x="category", y="count", title="Complaints by Category"), width="stretch")
with right:
    x = filtered.building.value_counts().reset_index()
    x.columns = ["building", "count"]
    st.plotly_chart(px.bar(x, x="building", y="count", title="Complaints by Building"), width="stretch")

left, right = st.columns(2)
with left:
    x = filtered.copy()
    x["created_date"] = pd.to_datetime(x.created_date)
    x = x.groupby(x.created_date.dt.to_period("M").astype(str)).size().reset_index(name="complaints")
    st.plotly_chart(px.line(x, x="created_date", y="complaints", markers=True, title="Monthly Complaint Trend"), width="stretch")
with right:
    x = energy.groupby("building", as_index=False).energy_kwh.sum().sort_values("energy_kwh", ascending=False)
    st.plotly_chart(px.bar(x, x="building", y="energy_kwh", title="Energy Consumption by Building"), width="stretch")

st.subheader("Issues Needing Attention")
st.dataframe(
    filtered[filtered.status != "Resolved"][
        ["complaint_id", "building", "category", "department", "priority", "status"]
    ].head(15),
    width="stretch",
    hide_index=True,
)

st.subheader("Ask CampusOps")
question = st.text_input("Ask about complaints, buildings, energy or equipment")
if question:
    st.info(answer_question(question))

st.caption("Synthetic data created for demonstration.")
