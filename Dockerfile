FROM apache/airflow:slim-2.8.0-python3.9

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    unset PIP_USER && pip install --no-cache-dir dbt-postgres==1.7.14 && deactivate

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER root
RUN sudo apt-get update && apt-get install postgresql-client-15 && apt-get install -y \
    curl \
    apt-transport-https \
    gnupg2

# Install mssql tools for bcp and sqlcmd
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
RUN sudo apt-get update
RUN sudo ACCEPT_EULA=Y apt-get -y install mssql-tools18 unixodbc-dev

RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
RUN source ~/.bashrc

RUN chown -R airflow /opt/airflow

USER airflow

ENV PATH="${PATH}:/opt/mssql-tools18/bin"