from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import bigquery


_ = load_dotenv()
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


plugin_directory = Path(__file__).parent.absolute()

KEY_FILE_PATH = plugin_directory / '*.json' # INSERT JSON FILE NAME
credentials = service_account.Credentials.from_service_account_file(
    str(KEY_FILE_PATH)
)
with open(str(KEY_FILE_PATH)) as f:
    import json
    key_data = json.load(f)
    project_id = key_data['project_id']


client = bigquery.Client(project=project_id, credentials=credentials)