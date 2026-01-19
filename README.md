# Monzo Banking Data Engineering Pipeline (BigQuery, DBT, Airflow, Docker)
An end-to-end ELT pipeline transforming raw Monzo banking API data into actionable financial insights. This project implements a Medallion Architecture on BigQuery, featuring Incremental Loading to optimise warehouse costs and processing time.

## Architecture Diagram
The following diagram illustrates the data flow from the Monzo API through the Google Cloud ecosystem, orchestrated by Airflow and transformed via dbt.

<img width="3379" height="1509" alt="Untitled-2026-01-18-0207" src="https://github.com/user-attachments/assets/d672f47a-a3ee-4490-a0a4-9d4abfbb0bb7" />

_Created in Excalidraw_

## Components

The pipeline orchestrates the flow from source API to data visualisation, ensuring data integrity at every place.

* **Extraction:** Python client fetches transactions; Great Expectations validates schema.
* **Loading:** Data is landed in BigQuery Bronze (Raw).
* **Transformation:** dbt manages the Silver (Cleaned) and Gold (Aggregated) layers.
* **Incremental Logic:** The Silver layer uses incremental materialisation, processing only new transactions since the last successful run to minimise BigQuery slot usage.
* **Orchestration:** Apache Airflow (Astronomer) handles the DAG lifecycle with integrated dbt execution via Cosmos.
* **Data Visualization:** Looker Studio serves as the exploration layer, allowing users to query the BigQuery Gold tables to uncover spending trends, merchant behaviors, and historical financial patterns through interactive dashboards.

## Key Technical Implementations

1. **Incremental Data Processing**

To handle financial data efficiently, dbt models are configured with a merge strategy. By using the is_incremental() macro, the pipeline avoids full-table refreshes, significantly reducing GCP compute costs.

2. **Multi-Layered Fail-Safes**

* **Phase 1 (Ingestion):** Custom Python alerts via Gmail/SMTP for API authentication or schema validation failures.

* **Phase 2 (Transformation):** dbt native tests (unique, not_null) coupled with Airflow's dependency management to stop the pipeline before bad data reaches the Gold layer.

3. **Containerised Local Development**
The entire stack is containerised using Docker and managed by Astronomer CLI, ensuring that the development environment is reproducible and 'cloud-ready'.

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

# 2. Securely place your GCP JSON key at:
- dbt_astro/dags/dbt_monzo_analytics/creds/your-service-account-key.json

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
Access the Airflow UI at http://127.0.0.1:8080

3. **Check service status**

```bash
astro dev logs --api-server
```

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
