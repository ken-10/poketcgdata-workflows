FROM apache/airflow:slim-2.8.0-python3.9
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER root
RUN sudo apt-get update && sudo apt-get install postgresql-client-15
RUN chown -R airflow /opt/airflow

USER airflow