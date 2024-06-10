import logging
import os
# import psycopg

from airflow.providers.postgres.hooks.postgres import PostgresHook
from common_packages import jinja_helper

_sql_query_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "sql"))


def bulk_load(connection_id: str, filepath: str, table: str, columns: str, file_format: str, delimiter=None,
              header_option=None):
    hook = PostgresHook(postgres_conn_id=connection_id)
    data = {
        'table': table,
        'columns': columns,
        'file_format': file_format,
    }
    if delimiter is not None:
        data['delimiter'] = delimiter
    if header_option is not None:
        data['header_option'] = header_option
    copy_cmd = jinja_helper.render_jinja2_template(_sql_query_path, 'copy_cmd.j2', data)
    hook.copy_expert(sql=copy_cmd, filename=filepath)
    logging.info(f"{filepath} bulk loaded into {table}")


def execute_query(connection_id: str, query: str, params=None):
    hook = PostgresHook(postgres_conn_id=connection_id)
    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            logging.info(f"Running query {query}")
            logging.info(f"Query params: {params}")
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

