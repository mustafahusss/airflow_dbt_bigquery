import os
from dag_utils import get_env_vars_from_connection


CONNECTION_NAME = 'db_conn'
DATASET = os.getenv("DATASET_ID")
SERVICE_ACCOUNT_VARIABLES = get_env_vars_from_connection(conn_id=CONNECTION_NAME)


PROFILES_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt_monzo_analytics/profiles.yml"
EXECUTION_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt_monzo_analytics"

# Set environment variables from the service account JSON fields
os.environ['project'] = SERVICE_ACCOUNT_VARIABLES.get('project_id', '')
os.environ['dataset'] = DATASET
os.environ['type'] = SERVICE_ACCOUNT_VARIABLES.get('type', '')
os.environ['project_id'] = SERVICE_ACCOUNT_VARIABLES.get('project_id', '')
os.environ['private_key_id'] = SERVICE_ACCOUNT_VARIABLES.get('private_key_id', '')
os.environ['private_key'] = SERVICE_ACCOUNT_VARIABLES.get('private_key', '')
os.environ['client_email'] = SERVICE_ACCOUNT_VARIABLES.get('client_email', '')
os.environ['client_id'] = SERVICE_ACCOUNT_VARIABLES.get('client_id', '')
os.environ['auth_uri'] = SERVICE_ACCOUNT_VARIABLES.get('auth_uri', '')
os.environ['token_uri'] = SERVICE_ACCOUNT_VARIABLES.get('token_uri', '')
os.environ['auth_provider_x509_cert_url'] = SERVICE_ACCOUNT_VARIABLES.get(
    'auth_provider_x509_cert_url', '')
os.environ['client_x509_cert_url'] = SERVICE_ACCOUNT_VARIABLES.get('client_x509_cert_url', '')