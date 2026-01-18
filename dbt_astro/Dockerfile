FROM astrocrpublic.azurecr.io/runtime:3.1-9

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery && deactivate

COPY dags/dbt_monzo_analytics/creds/project-424d7fe3-5b4f-48a0-a49-b28d32165ebb.json /app/creds/keyfile.json