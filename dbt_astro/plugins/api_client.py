import requests
from plugin_utils import MONZO_API_BASE, ACCESS_TOKEN, HEADERS
from google.cloud import bigquery
import json
from google.oauth2 import service_account
from google.cloud import bigquery



def get_method(suffix, params=None):
    url = MONZO_API_BASE + suffix
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

def get_account():
    url = MONZO_API_BASE + "/accounts"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_balance(account_id):
    url = MONZO_API_BASE + "/balance"
    response = requests.get(url, headers=HEADERS, params={"account_id": account_id})
    return response.json()


def get_transactions(account_id):
    url = MONZO_API_BASE + "/transactions"
    response = requests.get(url, headers=HEADERS, params={"account_id": account_id,
                                                          "limit": 100})
    return response.json()


def load_to_bigquery(df, table_name, project_id, dataset_id, client):
    table_id = f"{project_id}.{dataset_id}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    print(f"Loaded {len(df)} rows to {table_id}")

