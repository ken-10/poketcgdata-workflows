"""
Altered from https://www.astronomer.io/docs/learn/cleanup-dag-tutorial#:~:text=To%20keep%20your%20Airflow%20environment,DB%20without%20querying%20it%20directly.
DAG that will remove metadata older than given max age (in days) from airflow db. Default is anything older than 15 days.
Note that there is a global database statement timeout of 5 minutes, so if you have large tables you want to clean, you may need to run the cleanup in smaller batches."""

from datetime import timezone, datetime, timedelta

from airflow.cli.commands.db_command import all_tables
from airflow.decorators import dag, task
from airflow.models.param import Param
from airflow.operators.bash import BashOperator

UTC = timezone.utc
DRY_RUN = False


@dag(
    dag_id="db_cleanup",
    schedule_interval="15 0 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    is_paused_upon_creation=False,
    doc_md=__doc__,
    tags=['Maintanence', 'Metadata DB'],
    params={
        "max_metadata_age_in_days": Param(
            default=15,
            type="integer",
            description=f"Delete records older than the given number of days. Default is 15 days ago.",
        ),
        "tables": Param(
            default=[],
            type=["null", "array"],
            examples=all_tables,
            description="List of tables to clean. Default is all tables."
        ),
        "dry_run": Param(
            default=DRY_RUN,
            type="boolean",
            description="Print the SQL queries that would be run, but do not execute them. Default is False.",
        ),
    },
)
def db_cleanup():
    @task
    def get_timestamp_min_and_tables(**kwargs):
        tables = kwargs["params"]["tables"]
        max_metadata_age_in_days = kwargs["params"]["max_metadata_age_in_days"]
        clean_before_timestamp = datetime.now(tz=UTC) - timedelta(days=max_metadata_age_in_days)
        formatted_clean_before_timestamp = datetime.strftime(clean_before_timestamp, "%Y-%m-%dT%H:%M:%S%z")
        res = {"clean_before_timestamp": formatted_clean_before_timestamp,
               "tables": all_tables}
        if tables:
            res["tables"] = tables

        return res

    clean_db = BashOperator(
        task_id="clean_db",
        bash_command="""\
            airflow db clean \
             --clean-before-timestamp {{ ti.xcom_pull(task_ids="get_timestamp_min_and_tables")["clean_before_timestamp"] }} \
        {% if params.dry_run -%}
             --dry-run \
        {% endif -%}
             --skip-archive \
             --tables {{ ti.xcom_pull(task_ids="get_timestamp_min_and_tables")["tables"]|join(',') }} \
             --verbose \
             --yes \
        """,
        do_xcom_push=False,
    )
    get_timestamp_min_and_tables() >> clean_db


db_cleanup()
