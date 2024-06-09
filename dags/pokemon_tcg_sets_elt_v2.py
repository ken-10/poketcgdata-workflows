import os.path
import pendulum

from airflow.decorators import dag, task
from common_packages import config_helper, json_helper
from common_packages import api_helper, common_variables, file_helper, mssql_helper, discord_helper
from common_packages.dbt_cosmos.profiles import SqlServerUserPasswordProfileMapping
from common_packages.enums.APIResource import APIResource
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

_AIRFLOW_PATHS = common_variables.airflow_paths
_API_URL = common_variables.api_url
_DB_CONN_ID = "poketcgdata"
_DBT_EXECUTABLE_PATH = common_variables.dbt_executable_path
_MSSQL_DB_DRIVER = common_variables.mssql_driver


profile_config = ProfileConfig(
    profile_name="card_set",
    target_name="all",
    profile_mapping=SqlServerUserPasswordProfileMapping(
        conn_id="poketcgdata",
        profile_args={"schema": "cards",
                      "driver": _MSSQL_DB_DRIVER}
    ),
)

dbt_execution_config = ExecutionConfig(
    dbt_executable_path=_DBT_EXECUTABLE_PATH,
)


def send_failure_alert(context):
    webhook = config_helper.get_config("discord_webhook")
    ti = context.get("task_instance")
    discord_helper.send_failure_message(webhook_link=webhook, dag_id=ti.dag_id, task_id=ti.task_id, log_url=ti.log_url,
                                        run_id=ti.run_id)


@dag(
    schedule='*/30 * * * *',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ELT", "POKEMON", "SET", "MSSQL"],
    max_active_runs=1
)
def pokemon_tcg_sets_elt_v2():
    @task(on_failure_callback=send_failure_alert)
    def get_sets_from_api():
        processing_folder = file_helper.create_folder(_AIRFLOW_PATHS["dags_data"], "pokemon_tcg_sets_load_v2")
        api_key = config_helper.get_config("pokemon_tcg_api")["key"]
        sets_payload = api_helper.get_all(api_url=_API_URL, api_key=api_key, resource=APIResource.SETS)
        sets_csv = os.path.join(processing_folder, "pokemon_tcg_sets.csv")
        sets_csv = json_helper.json_to_csv_for_mssql(output_path=sets_csv, json_data=sets_payload)
        return {"processing_folder": processing_folder, "sets_csv": sets_csv}

    @task(on_failure_callback=send_failure_alert)
    def truncate_landing_table():
        mssql_helper.execute_query(_DB_CONN_ID, 'TRUNCATE TABLE cards.ldg_card_set;')

    @task(on_failure_callback=send_failure_alert)
    def bulk_copy_to_landing_table(**kwargs):
        sets_csv = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id,
                                          task_ids="get_sets_from_api")["sets_csv"]
        mssql_helper.bcp_file_to_table(conn_id=_DB_CONN_ID, schema="cards", table="ldg_card_set",
                                       file_path=sets_csv)

    @task(on_failure_callback=send_failure_alert)
    def remove_folder_and_contents(**kwargs):
        processing_folder = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id, task_ids="get_sets_from_api")[
            "processing_folder"]
        file_helper.delete_folder(processing_folder)

    dbt_transfrom = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(os.path.join(_AIRFLOW_PATHS["dbt"]["poketcgdata_mssql"], "card_sets")),
        profile_config=profile_config,
        execution_config=dbt_execution_config,
        default_args={
            'on_failure_callback': send_failure_alert
        }
    )

    (
            get_sets_from_api()
            >> truncate_landing_table()
            >> bulk_copy_to_landing_table()
            >> remove_folder_and_contents()
            >> dbt_transfrom
    )


pokemon_tcg_sets_elt_v2()
