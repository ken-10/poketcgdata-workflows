import os.path
import pendulum

from airflow.decorators import dag, task
from common_packages import config_helper, json_helper
from common_packages import api_helper, common_variables, file_helper, postgresql_helper
from common_packages.enums.APIResource import APIResource
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.operators import DbtDocsOperator

_AIRFLOW_PATHS = common_variables.airflow_paths
_API_URL = common_variables.api_url
_DBT_EXECUTABLE_PATH = common_variables.dbt_executable_path

profile_config = ProfileConfig(
    profile_name="poketcgdata",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="poketcgdata_dev",
        profile_args={"schema": "cards"},
    ),
)

dbt_execution_config = ExecutionConfig(
    dbt_executable_path=_DBT_EXECUTABLE_PATH,
)


def failure_cleanup(context):
    processing_folder = context["ti"].xcom_pull(dag_id=context["dag_run"].dag_id, task_ids="get_sets_from_api")["processing_folder"]
    file_helper.delete_folder(processing_folder)


@dag(
    schedule='0 */2 * * *',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ELT", "POKEMON", "CARD", "PRICES"],
)
def pokemon_tcg_card_prices_elt():
    @task(on_failure_callback=failure_cleanup)
    def get_card_details_from_api():
        processing_folder = file_helper.create_folder(_AIRFLOW_PATHS["dags_data"], "pokemon_tcg_card_prices_load")
        api_key = config_helper.get_config("pokemon_tcg_api")["key"]
        sets_payload = api_helper.get_all(api_url=_API_URL, api_key=api_key, resource=APIResource.CARDS)
        cards_csv = os.path.join(processing_folder, "pokemon_tcg_cards.csv")
        cards_csv = json_helper.json_to_csv(output_path=cards_csv, json_list=sets_payload)
        return {"processing_folder": processing_folder, "cards_csv": cards_csv}

    @task(on_failure_callback=failure_cleanup)
    def truncate_landing_table():
        postgresql_helper.execute_query('poketcgdata_dev', 'TRUNCATE TABLE cards.card_price_ldg;')

    @task(on_failure_callback=failure_cleanup)
    def bulk_copy_to_landing_table(**kwargs):
        sets_csv = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id, task_ids="get_card_details_from_api")["cards_csv"]
        postgresql_helper.bulk_load("poketcgdata_dev", sets_csv, "cards.card_price_ldg", "raw_json", "csv")

    @task(on_failure_callback=failure_cleanup)
    def remove_folder_and_contents(**kwargs):
        processing_folder = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id, task_ids="get_card_details_from_api")[
            "processing_folder"]
        file_helper.delete_folder(processing_folder)

    dbt_transfrom = DbtTaskGroup(
        group_id="transform_data_to_target_table",
        project_config=ProjectConfig(os.path.join(_AIRFLOW_PATHS["dbt"]["poketcgdata"], "card_prices")),
        profile_config=profile_config,
        execution_config=dbt_execution_config,
    )

    (
            get_card_details_from_api()
            >> truncate_landing_table()
            >> bulk_copy_to_landing_table()
            >> dbt_transfrom
    )


pokemon_tcg_card_prices_elt()
