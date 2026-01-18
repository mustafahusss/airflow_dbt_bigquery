import pandas as pd
from google.cloud import bigquery
import great_expectations as gx
from plugin_utils import create_dataframe, setup_validation, run_validation, load_data, send_email_failure

def app_runner():
    dataframes = create_dataframe()

    balance_df = dataframes['balance_df']
    accounts_df = dataframes['accounts_df']
    transactions_df_clean = dataframes['transactions_df_clean']

    batch = setup_validation(transactions_df_clean)
    data_checks = run_validation(batch)

    if data_checks['all_passed']:

        print("checks passed")
        print("loading data to bigquery...")

        load_data(accounts_df, transactions_df_clean, balance_df)

    else:
        print("some checks failed")
        print("data will not be loaded to bigquery")
        print("please review failed great_expectations checks above and fix the issues")

        send_email_failure(data_checks)

        print("Failure notification email sent")



if __name__ == "__main__":
    app_runner()
