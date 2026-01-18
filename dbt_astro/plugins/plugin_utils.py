from api_client import *
import pandas as pd
import great_expectations as gx
from email.message import EmailMessage
import datetime
from env_variables import *
import smtplib
from plugin_variables import *


def fetch_account_data():
    accounts_data = get_account()
    accounts_list = accounts_data.get('accounts', [])

    if not accounts_list:
        print("No accounts found for this user.")
        return None

    account_id = accounts_list[0]["id"]

    return {
        'accounts_list': accounts_list,
        'account_id': account_id
    }

def fetch_raw_data(account_id):

    balance_data = get_balance(account_id)
    transactions_data = get_transactions(account_id)
    transactions_list = transactions_data['transactions']

    return {
        'transactions_list': transactions_list,
        'balance_data': balance_data,
    }

def create_dataframe():
    accounts_data = fetch_account_data()
    account_id = accounts_data['account_id']

    raw_data = fetch_raw_data(account_id)

    accounts_list = accounts_data['accounts_list']
    balance_data = raw_data['balance_data']
    transactions_list = raw_data['transactions_list']


    balance_df = pd.DataFrame([balance_data])
    accounts_df = pd.DataFrame(accounts_list)
    transactions_df_clean = clean_transactions(transactions_list)

    return {
        'accounts_df': accounts_df,
        'balance_df': balance_df,
        'transactions_df_clean': transactions_df_clean
    }


def clean_transactions(transactions_list):

    transactions_df = pd.DataFrame(transactions_list)
    columns_to_drop = ['fees', 'metadata', 'counterparty', 'attachments', 'labels',
                       'categories', 'international', 'atm_fees_detailed']
    transactions_df_stg = transactions_df.drop(columns=columns_to_drop, errors='ignore')

    return transactions_df_stg



def setup_validation(dataframe):
    # Step 1: Create a context (i.e., give access to GX)
    context = gx.get_context()

    # Step 2: Tell GX about the Pandas data source
    data_source = context.data_sources.add_pandas(name="my_pandas_data")

    # Step 3: Tell GX about a specific dataframe
    data_asset = data_source.add_dataframe_asset(name="transactions")

    # Step 4: Create a 'batch' (this is the actual data that will be checked)
    batch_definition = data_asset.add_batch_definition_whole_dataframe("transactions_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": dataframe})

    return batch

def run_validation(batch):
    expectation1 = gx.expectations.ExpectColumnToExist(column="id")
    expectation2 = gx.expectations.ExpectColumnValuesToNotBeNull(column="id")
    expectation3 = gx.expectations.ExpectColumnValuesToBeUnique(column="id")
    expectation4 = gx.expectations.ExpectColumnValuesToNotBeNull(column="amount")
    expectation5 = gx.expectations.ExpectColumnValuesToNotBeNull(column="created")

    result1 = batch.validate(expectation1)
    result2 = batch.validate(expectation2)
    result3 = batch.validate(expectation3)
    result4 = batch.validate(expectation4)
    result5 = batch.validate(expectation5)

    return {
        'id_exists': result1.success,
        'id_not_null': result2.success,
        'id_unique': result3.success,
        'amount_not_null': result4.success,
        'created_not_null': result5.success,
        'all_passed': result1.success and result2.success and result3.success and result4.success and result5.success
    }


def send_email_failure(results):
    email_content = f"""
    Data Quality Checks Failed

    Validation Results:
    - ID exists: {results['id_exists']}
    - No null values in ID:  {results['id_not_null']}
    - Values in ID are unique: {results['id_unique']}
    - No null values in amount: {results['amount_not_null']}
    - No null values in created: {results['created_not_null']}

    Please review and fix the issues before data can be loaded to BigQuery.
    """

    context = gx.get_context()
    message = EmailMessage()
    message["To"] = "*@gmail.com"  # INSERT YOUR GMAIL ADDRESS
    message["From"] = "*@gmail.com" # INSERT YOUR GMAIL ADDRESS
    x = datetime.datetime.now()
    message["Subject"] = f"Python Failure - {x.strftime('%Y-%m-%d %H:%M:%S')}"
    message.set_content(email_content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
        smtp.send_message(message)

def load_data(accounts_df, transactions_df_clean, balance_df):

    # Delete tables before loading
    tables_to_truncate = ["raw_accounts", "raw_transactions", "raw_balance"]
    for table_name in tables_to_truncate:
        table_id = f"{project_id}.{DATASET_ID}.{table_name}"
        client.delete_table(table_id, not_found_ok=True)
        print(f"Deleted table {table_id}")

    # Now load the data
    load_to_bigquery(accounts_df, "raw_accounts", project_id, DATASET_ID, client)
    load_to_bigquery(transactions_df_clean, "raw_transactions", project_id, DATASET_ID, client)
    load_to_bigquery(balance_df, "raw_balance", project_id, DATASET_ID, client)