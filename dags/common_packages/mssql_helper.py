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


def bcp_file_to_table(database: str, schema: str, table: str, file_path: str, server: str, username: str, password: str,
                      field_terminator=None, char_data_type=None, row_terminator=None):
    # TODO: Modify function to get attributes from airflow connection
    logging.info(f'Attempting to bulk copy {file_path} to {database}.{schema}.{table}')
    cmd_prefix = f'bcp {database}.{schema}.{table} in {file_path}'
    cmd_suffix = f'-S {server} -U {username} -P {password}'
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
