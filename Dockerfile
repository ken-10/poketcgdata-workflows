FROM apache/airflow:slim-2.8.0-python3.9

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    unset PIP_USER && pip install --no-cache-dir dbt-postgres==1.7.14 && deactivate

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER root
RUN sudo apt-get update && sudo apt-get install postgresql-client-15
RUN chown -R airflow /opt/airflow

USER airflow