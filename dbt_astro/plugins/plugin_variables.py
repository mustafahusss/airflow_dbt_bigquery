from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import bigquery
from env_variables import ACCESS_TOKEN

load_dotenv(find_dotenv())

plugin_dir = Path(__file__).parent.absolute()
BASE_DIR = plugin_dir.parent

KEY_FILE_PATH = (
    BASE_DIR /
    "dags/dbt_monzo_analytics/creds/*.json" # INSERT SERVICE ACCOUNT JSON KEY HERE
)

credentials = service_account.Credentials.from_service_account_file(str(KEY_FILE_PATH))

client = bigquery.Client(project=credentials.project_id, credentials=credentials)

MONZO_API_BASE = "https://api.monzo.com"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
