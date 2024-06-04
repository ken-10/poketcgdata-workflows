import logging
import subprocess
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook


def execute_query(conn_id: str, sql_query: str, params=None):
    hook = MsSqlHook(mssql_conn_id=conn_id)
    with hook.get_conn() as conn:
        with conn.cursor() as csr:
            if not params:
                params = ()
            logging.info(f"Executing given query with params: {params}")
            csr.execute(sql_query, params)
            conn.commit()
            logging.info(f"Executed query")


def bcp_file_to_table(conn_id: str, schema: str, table: str, file_path: str, field_terminator=None, char_data_type=None,
                      row_terminator=None):
    from airflow.models.connection import Connection
    from airflow.utils.log.secrets_masker import mask_secret
    conn = Connection.get_connection_from_secrets(conn_id)
    database = conn.schema
    username = conn.login
    password = conn.password
    mask_secret([username, password])
    logging.info(f'Using connection ID {conn_id} to bulk copy {file_path} to {database}.{schema}.{table}')
    cmd_prefix = f'bcp {database}.{schema}.{table} in {file_path}'
    cmd_suffix = f'-S {conn.host} -U {username} -P {password}'
    cmd_options = '-c'
    if char_data_type:
        cmd_options += f' {char_data_type}'
    if field_terminator:
        cmd_options += f' -t{field_terminator}'
    if row_terminator:
        cmd_options += f' -r {row_terminator}'

    final_cmd = f"{cmd_prefix} {cmd_options} {cmd_suffix}"
    subprocess.run(final_cmd, shell=True)
    logging.info(f'Successfully bulk copied {file_path} to {database}.{schema}.{table}')

    return final_cmd
