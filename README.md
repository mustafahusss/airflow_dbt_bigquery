# Monzo Banking Data Engineering Project (BigQuery, DBT, Airflow, Docker)
A data engineering project leveraging data from Monzo's API built on BigQuery visualised in Looker, running locally with Astronomer and Docker.

## Architecture Diagram


Created in Excalidraw

## Components
* **API:** Monzo banking data source
* **Extract & Load:** Python with Great Expectations for extraction and data quality validation
* **Data Warehouse:** BigQuery medallion architecture (Bronze → Silver → Gold layers)
* **Test & Transform:** dbt for SQL transformations and testing
* **Orchestrator:** Airflow pipeline scheduling and execution
* **Data Visualization:** Looker dashboards for analysis and forecasting
* **Container:** Docker deployment environment
* **Email Alert:** Failure notification system

## Project Structure
airflow_dbt_bigquery/
├── Dockerfile                      # Docker container configuration
├── airflow_settings.yaml           # Airflow configuration
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .gitignore                      
├── dbt_astro/
│   ├── dags/
│   │   ├── dbt_monzo_analytics/    # dbt project root
│   │   │   ├── models/             # dbt transformation models (staging, marts)
│   │   │   ├── tests/              # dbt data quality tests
│   │   │   └── dbt_project.yml     # dbt project configuration
│   │   ├── dag_monzo.py            # Airflow DAG definition
│   │   └── requirements.txt        # DAG dependencies
│   ├── plugins/
│   │   ├── main.py                 # Monzo API extraction and loading
│   │   ├── api_client.py           # Monzo API client
│   │   └── env_variables.py        # Environment configuration
│   └── tests/                      # Great Expectations data validation
└── .venv1/                         # Python virtual environment

