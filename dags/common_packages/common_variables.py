api_url = 'https://api.pokemontcg.io/v2'

airflow_paths = {
    'sql_queries': '/opt/airflow/common_packages/resources/sql',
    'dags_data': '/opt/airflow/dags_data',
    'dbt': {
        'base': '/opt/airflow/dags/dbt',
        'poketcgdata': '/opt/airflow/dags/dbt/poketcgdata'
    }
}

dbt_executable_path = '/opt/airflow/dbt_venv/bin/dbt'