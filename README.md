# Monzo Banking Data Engineering Project (BigQuery, DBT, Airflow, Docker)

## Overview
This project illustrates how to integrate data from your Monzo's API into a BigQuery database. 
The pipeline leverages Python for extraction, DBT for transformation, and Airflow for orchestration to ensure reliability and scalability.

## Architecture
**Python**: Extracts data from Monzo API.

**Great Expectation**: Handles data quality testing before loading to the data warehouse.

**BigQuery**: Cloud data warehouse for storage and analytics, following medallion architecture (Bronze → Silver → Gold).

**DBT**: Handles SQL-based data transformations and data quality tests in BigQuery.

**Airflow**: Orchestrates and schedules the end-to-end process including Python extraction and DBT runs using Astronomer Cosmos.

**Looker**: Google's native Business intelligence tool to do trend analysis and forecasting.

<img width="3379" height="1509" alt="Untitled-2026-01-18-0207" src="https://github.com/user-attachments/assets/d2d47ac9-83c1-4c89-973c-5f4f462b1ac7" />

## Prerequisites
* Monzo Developer Account
* Python 3.14 or higher
* Google Cloud Account 
  * BigQuery Database
  * Google Service Account 
* DBT CLI
* Apache Airflow
* Docker Desktop
* Cosmos from Astronomer

## Instructions
1. Clone the repository
```bash
git clone https://github.com/<your-username>/airflow_dbt_bigquery.git
cd bigquery-dbt-monzo
```

2. Create a dataset in BigQuery

Update the placeholders for dataset name in the following locations:
- airflow_dbt_bigquery/dbt_astro/dags/dag_variables.py
- airflow_dbt_bigquery/dbt_astro/.env

A '.env' file needs to be created here and the variable should follow this naming convention without the brackets:

```python
DATASET_ID = "{DATASET NAME}"
```

3. Create a Google Service Account

A service account enables the GCP Admin to apply the principle of least privilege, where the service account is only given the necessary permissions required for the project.

```bash
# 1. Create a service account in GCP Console
- Go to: IAM & Admin > Service Accounts > Create Service Account

# 2. Grant BigQuery permissions:
- BigQuery Admin (or BigQuery Data Editor + BigQuery Job User)
```

Grant minimum required permissions to the service account (principle of least privilege):
  - `BigQuery Data Editor` for data manipulation
  - `BigQuery Job User` for running queries
  - Avoid `BigQuery Admin` unless necessary


4. Create and download the JSON key associated to your service account 

The JSON key contains all the necessary details required for the script to connect to BigQuery.

```bash
# 1. Create and download JSON key
- Click on service account > Keys > Add Key > Create New Key > JSON

# 2. Place a key file in each of the project folders below:
- dbt_astro/dags/dbt_monzo_analytics/creds/{GCP SERVICE ACCOUNT}.json
- dbt_astro/plugins/{GCP SERVICE ACCOUNT}.json

# 3. Update Dockerfile to include the name of your service account name
COPY dags/dbt_monzo_analytics/creds/{GCP SERVICE ACCOUNT}.json /app/creds/keyfile.json

# 4. Restart Docker
docker-compose down
docker-compose up -d
```

5. Obtain a Monzo API key

Monzo's API key is accessible from this website - https://developers.monzo.com

_Note: This key must be updated before the scheduled refresh. This is refreshed weekly but if you require a daily or hourly refresh you may want to use a refresh token._

6. Add an Airflow connection ID

In Airflow navigate to:
```bash
Admin Settings > Add Connection > Connection Type > Select Google BigQuery > Open Extra Fields > Insert Project ID from BigQuery and the raw keyfile JSON
```
Insert the connection id in the following location:

PycharmProjects/airflow_dbt_bigquery/dbt_astro/dags/dag_variables.py

```python
CONNECTION_NAME = '{INSERT AIRFLOW CONNECTION NAME HERE}' 
```
_Note: to open Airflow ensure Docker Desktop is running then run the 'astro dev start' command in your terminal_

## Debugging
### Rotate API Keys
Currently the user must update the Monzo API token manually for each refresh.

### Astro dev start - timeout
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

### Port Conflicts
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

## Security Considerations
### Service Account Authentication
Personal Google accounts cannot be used in Docker containers and should never be hardcoded. Service accounts are used instead providing secure access with auditable credentials.

- Always use GCP Service Accounts for authentication (see instructions section for setup)
- Grant minimum required permissions (principle of least privilege):
  - `BigQuery Data Editor` for data manipulation
  - `BigQuery Job User` for running queries
  - Avoid `BigQuery Admin` unless necessary
- Never commit service account JSON keys to version control

### Credential Management
These are the service account details extracted from the previous step. They are referenced in our code but shouldn't be committed into the final code.
```bash
# Add to .gitignore
*.json
*.key
.env
airflow.cfg
```

### Environment Variables
Store sensitive values in environment variables, never in code:
```bash
# .env (not committed to git)
MONZO_CLIENT_ID=your_client_id
MONZO_CLIENT_SECRET=your_client_secret
GCP_PROJECT_ID=your_project_id
```
