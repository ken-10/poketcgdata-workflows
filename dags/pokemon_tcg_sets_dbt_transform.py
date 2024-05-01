from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from datetime import datetime

profile_config = ProfileConfig(
    profile_name="poketcgdata",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="poketcgdata_dev",
        profile_args={"schema": "cards"},
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "/opt/airflow/dags/dbt/poketcgdata/card_sets",
    ),
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path='/opt/airflow/dbt_venv/bin/dbt',
    ),
    # normal dag parameters
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="pokemon_tcg_sets_dbt_transform",
    tags=["ELT", "POKEMON", "SET"],
    default_args={}
)
