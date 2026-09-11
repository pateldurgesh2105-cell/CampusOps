# CampusOps

CampusOps is a small data engineering and analytics project built around a realistic college operations scenario.

It processes maintenance complaints, energy usage, equipment records, and room utilization data to identify recurring issues, unresolved work, and operational patterns.

## Live Dashboard

https://campusops-bpwmwfvsdqmkgfgxcyutyw.streamlit.app/

## Features
- Data cleaning and validation
- Duplicate complaint removal
- Complaint and department analysis
- Energy usage analysis
- Equipment maintenance tracking
- Streamlit dashboard
- Lightweight NLP question answering using TF-IDF similarity
- Pytest checks
- Airflow pipeline example

## Tech Stack
Python • Pandas • SQL • Scikit-learn • Streamlit • Plotly • Pytest • Apache Airflow

## Run

```bash
pip install -r requirements.txt
python src/data_pipeline.py
python -m streamlit run dashboard.py
```

Run tests:
```bash
pytest -q
```

## Data
Synthetic data is included to simulate a college operations environment.

## Author
Durgesh Patel
