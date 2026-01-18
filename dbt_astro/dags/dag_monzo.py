"""Module providing an Airflow Dag Implementation"""
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ExecutionConfig, ProjectConfig, ProfileConfig
from pathlib import Path
from main import app_runner
from dag_variables import PROFILES_PATH, EXECUTION_PATH, PROJECT_PATH

profile = ProfileConfig(
    profile_name='dbt_monzo_analytics',
    target_name='dev',
    profiles_yml_filepath=Path(PROFILES_PATH)
)

execution_config = ExecutionConfig(
     dbt_executable_path=EXECUTION_PATH,
)

with DAG(
    dag_id="monzo_to_bigquery_pipeline",
    start_date=datetime(2026, 1, 9),
    schedule="@daily",
    catchup=False,
) as dag:
    extract_and_load = PythonOperator(
        task_id="extract_monzo_data",
        python_callable=app_runner,
    )
    transform_data = DbtTaskGroup(
        group_id="dbt_transformation",
        project_config=ProjectConfig(PROJECT_PATH),
        profile_config=profile,
        execution_config=execution_config,
    )

    extract_and_load >> transform_data