import os.path
import pendulum

from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from common_packages import config_helper, json_helper
from common_packages import api_helper, common_variables, file_helper, postgresql_helper
from common_packages.enums.APIResource import APIResource

_AIRFLOW_PATHS = common_variables.airflow_paths
_API_URL = common_variables.api_url

def failure_cleanup(context):
    processing_folder = context["ti"].xcom_pull(dag_id=context["dag_run"].dag_id, task_ids="get_sets_from_api")["processing_folder"]
    file_helper.delete_folder(processing_folder)

@dag(
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ELT", "POKEMON", "SET"],
)
def pokemon_tcg_sets_extract_load():
    @task(on_failure_callback=failure_cleanup)
    def get_sets_from_api():
        processing_folder = file_helper.create_folder(_AIRFLOW_PATHS["dags_data"], "pokemon_tcg_sets_load")
        api_key = config_helper.get_config("pokemon_tcg_api")["key"]
        sets_payload = api_helper.get_all(api_url=_API_URL, api_key=api_key, resource=APIResource.SETS)
        sets_csv = os.path.join(processing_folder, "pokemon_tcg_sets.csv")
        sets_csv = json_helper.json_to_csv(output_path=sets_csv, json_list=sets_payload)
        return {"processing_folder": processing_folder, "sets_csv": sets_csv}

    @task(on_failure_callback=failure_cleanup)
    def truncate_landing_table(**kwargs):
        postgresql_helper.execute_query('poketcgdata_dev', 'TRUNCATE TABLE cards.card_set_ldg;')

    @task(on_failure_callback=failure_cleanup)
    def bulk_copy_to_landing_table(**kwargs):
        sets_csv = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id, task_ids="get_sets_from_api")["sets_csv"]
        postgresql_helper.bulk_load("poketcgdata_dev", sets_csv, "cards.card_set_ldg", "raw_json", "csv")

    @task(on_failure_callback=failure_cleanup)
    def remove_folder_and_contents(**kwargs):
        processing_folder = kwargs["ti"].xcom_pull(dag_id=kwargs["dag_run"].dag_id, task_ids="get_sets_from_api")[
            "processing_folder"]
        file_helper.delete_folder(processing_folder)

    trigger_dbt_transform_dag = TriggerDagRunOperator(
        task_id='trigger_dbt_transform_dag',
        trigger_dag_id='pokemon_tcg_sets_dbt_transform'
    )

    get_sets_from_api() >> truncate_landing_table() >> bulk_copy_to_landing_table() >> remove_folder_and_contents() >> trigger_dbt_transform_dag

pokemon_tcg_sets_extract_load()