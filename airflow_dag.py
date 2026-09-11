from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    "campusops_daily_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    process = BashOperator(
        task_id="process_data",
        bash_command="python src/data_pipeline.py",
    )
    quality = BashOperator(
        task_id="quality_checks",
        bash_command="python src/data_quality.py",
    )
    process >> quality
