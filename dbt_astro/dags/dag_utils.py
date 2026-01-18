from airflow.sdk import Connection
import json

def get_env_vars_from_connection(conn_id: str):
    """
    Fetches the Google Cloud service account credentials
    from Airflow connection and sets them as environment variables.

    Args:
        conn_id: Airflow connection ID

    Return:
        service_account_dict: Dictionary of service account credentials
    """
    # Fetch connection details from Airflow
    conn  = Connection.get(conn_id=conn_id)
    keyfile_json = conn.extra_dejson.get('keyfile_dict')

    # Load the service account JSON into a dictionary
    if isinstance(keyfile_json, str):
        service_account_dict = json.loads(keyfile_json)
    else:
        service_account_dict = keyfile_json

    return service_account_dict