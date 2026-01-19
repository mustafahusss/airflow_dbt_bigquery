# Monzo Banking Data Engineering Project (BigQuery, DBT, Airflow, Docker)
An end-to-end data engineering project built using Google Cloud Platform leveraging data from Monzo's API built on BigQuery visualised in Looker, running locally with Astronomer and Docker.

## Architecture Diagram

<img width="3379" height="1509" alt="Untitled-2026-01-18-0207" src="https://github.com/user-attachments/assets/d672f47a-a3ee-4490-a0a4-9d4abfbb0bb7" />

_Created in Excalidraw_

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

```bash
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
```

## Start Guide

### Prerequisites

---

* Docker Desktop
* Docker Compose
* Monzo API Key
* Google Cloud Account (free trial)
* Gmail Account & App Password (optional)

### Files Setup

---

**.env file**
```bash
ACCESS_TOKEN = your-monzo-api-key
DATASET_ID = your-bigquery-dataset-name
GMAIL_ACCOUNT = your-gmail-address
GMAIL_PASSWORD = your-gmail-app-password
```
**Service Account JSON Key**
```bash
# 1. Create and download JSON key
- Click on service account > Keys > Add Key > Create New Key > JSON

# 2. Place a key file in each of the project folders below:
- dbt_astro/dags/dbt_monzo_analytics/creds/{GCP SERVICE ACCOUNT}.json

# 3. Update Dockerfile in the root folder to include the name of your service account name
COPY dags/dbt_monzo_analytics/creds/your-service-account-key.json /app/creds/keyfile.json
```

### Setup

---

1. **Clone the repository**
```bash
git clone https://github.com/[insert_username]/airflow_dbt_bigquery
cd airflow_dbt_bigquery
```

2. **Start the platform**
```bash
astro dev start
```

3. **Access Services**
* Airflow: http://127.0.0.1:8080

### Component Status

---

1. Check service status

```bash
astro dev logs --api-server
```

### Components

---

#### Monzo API Client
* Authenticates and connects to Monzo banking API
* Retrieves transaction and account data
* Handles API rate limiting and error responses

#### Extract & Load Pipeline

* Python-based data extraction from Monzo API
* Great Expectations validation for data quality checks
* Loads raw data into BigQuery Bronze layer

#### dbt Transformations

* SQL-based transformations across medallion layers
* Staging models clean and standardise raw data
* Marts models create business-ready analytics tables
* Built-in data quality tests and documentation

#### Airflow Orchestrator

* Schedules and manages end-to-end pipeline execution
* Integrates Python extraction with dbt runs via Astronomer Cosmos
* Email alerts for pipeline failures
* Configurable retry logic and dependencies

#### Looker Dashboards
* Interactive visualizations for spending analysis
* Trend analysis and forecasting capabilities
* Direct connection to BigQuery Gold layer
* Users can build custom dashboards based on their preferences and requirements

### Troubleshooting

---

#### Rotate API Keys
Currently the user must update the Monzo API token manually for each refresh.

#### Astro dev start - timeout
When running the 'astro dev start' command the system almost always returns a timed out prompt similar to that below:

```bash
 astro dev start
✔ Project image has been updated
Error: There might be a problem with your project starting up. The api-server health check timed out after 1m0s but your project will continue trying to start. Run 'astro dev logs --api-server | --scheduler' for details.
Try again or use the --wait flag to increase the time out
```
To check whether the script failed run the following command 'astro dev logs --api-server'. 

If you see this then the script successfully ran and you can click the link to access Airflow. 

```bash
2026-01-18T00:22:17.200399000ZINFO:     Application startup complete.
2026-01-18T00:22:17.200402000ZINFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```
If you  saw a failure then you will  have to use the response to troubleshoot the issue.

#### Port Conflicts
In some instances Port 8080 may appear as already in use stopping Airflow webserver from starting. To resolve this you can following some of the options below:

```bash
# Check what's using port 8080
lsof -i :8080                    # macOS/Linux
netstat -ano | findstr :8080     # Windows

# Kill process on port 8080
lsof -ti:8080 | xargs kill -9    # macOS/Linux
taskkill /PID  /F           # Windows

# Or use different port
airflow webserver --port 8000
```
