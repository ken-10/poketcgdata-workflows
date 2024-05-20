from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook


def bulk_copy(conn_id: str, table: str, elements_to_insert: list, column_ids: list = None, tablock: bool = False,
              batch_size: int = 1000):
    hook = MsSqlHook(mssql_conn_id=conn_id)
    with hook.get_conn() as conn:
        conn.bulk_copy(table_name=table, elements=elements_to_insert, column_ids=column_ids, batch_size=batch_size,
                       tablock=tablock)
