"""
Tests for the sql server profile.
Adapted from: https://github.com/astronomer/astronomer-cosmos/blob/main/tests/profiles/postgres/test_pg_user_pass.py
"""

from unittest.mock import patch

import pytest
from airflow.models.connection import Connection

from dags.common_packages.dbt_cosmos.profiles import get_automatic_profile_mapping, SqlServerUserPasswordProfileMapping

# TODO: clean up tests

@pytest.fixture()
def mock_mssql_conn():  # type: ignore
    """
    Sets the connection as an environment variable.
    """
    conn = Connection(
        conn_id="mock_mssql",
        conn_type="mssql",
        host="my_host",
        login="my_user",
        password="my_password",
        port=1433,
        schema="my_database"
    )

    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        yield conn


@pytest.fixture()
def mock_mssql_conn_custom_port():  # type: ignore
    """
    Sets the connection as an environment variable.
    """
    conn = Connection(
        conn_id="mock_mssql",
        conn_type="mssql",
        host="my_host",
        login="my_user",
        password="my_password",
        port=7472,
        schema="my_database",
    )

    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        yield conn


@pytest.fixture()
def mock_mssql_conn_custom_driver():  # type: ignore
    """
    Sets the connection as an environment variable.
    """
    conn = Connection(
        conn_id="mock_mssql",
        conn_type="mssql",
        host="my_host",
        login="my_user",
        password="my_password",
        port=7472,
        schema="my_database"
    )

    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        yield conn


def test_connection_claiming() -> None:
    """
    Tests that the mssql profile mapping claims the correct connection type.
    """
    # should only claim when:
    # - conn_type == mssql
    # and the following exist:
    # - host
    # - user
    # - password
    # - port
    # - dbname or database
    # - schema
    potential_values = {
        "conn_type": "mssql",
        "host": "my_host",
        "login": "my_user",
        "password": "my_password",
        "schema": "my_schema",
        "database": "my_db"
    }

    # if we're missing any of the values, it shouldn't claim
    for key in potential_values:
        values = potential_values.copy()
        del values[key]
        conn = Connection(**values)  # type: ignore

        print("testing with", values)

        with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
            profile_mapping = SqlServerUserPasswordProfileMapping(conn, {"schema": "my_schema"})
            assert not profile_mapping.can_claim_connection()

    # also test when there's no schema
    conn = Connection(**{k: v for k, v in potential_values.items() if k != "schema"})
    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        profile_mapping = SqlServerUserPasswordProfileMapping(conn, {"schema": None})
        assert not profile_mapping.can_claim_connection()

    # if we have them all, it should claim
    conn = Connection(**potential_values)  # type: ignore
    with patch("airflow.hooks.base.BaseHook.get_connection", return_value=conn):
        profile_mapping = SqlServerUserPasswordProfileMapping(conn, {"schema": "my_schema"})
        assert profile_mapping.can_claim_connection()


def test_profile_mapping_selected(
    mock_mssql_conn: Connection,
) -> None:
    """
    Tests that the correct profile mapping is selected.
    """
    profile_mapping = get_automatic_profile_mapping(
        mock_mssql_conn.conn_id,
        {"schema": "my_schema",
         "driver": "ODBC Driver 18 for SQL Server"}
    )
    assert isinstance(profile_mapping, SqlServerUserPasswordProfileMapping)


def test_profile_mapping_keeps_custom_port(mock_mssql_conn_custom_port: Connection) -> None:
    profile = SqlServerUserPasswordProfileMapping(mock_mssql_conn_custom_port.conn_id, {"schema": "my_schema"})
    assert profile.profile["port"] == 7472


def test_profile_args(
    mock_mssql_conn: Connection,
) -> None:
    """
    Tests that the profile values get set correctly.
    """
    profile_mapping = get_automatic_profile_mapping(
        mock_mssql_conn.conn_id,
        profile_args={"schema": "my_schema"},
    )
    assert profile_mapping.profile_args == {
        "schema": "my_schema",
    }

    assert profile_mapping.profile == {
        "type": mock_mssql_conn.conn_type,
        "host": mock_mssql_conn.host,
        "user": mock_mssql_conn.login,
        "password": "{{ env_var('COSMOS_CONN_MSSQL_PASSWORD') }}",
        "port": mock_mssql_conn.port,
        "schema": "my_schema",
    }


def test_profile_env_vars(
    mock_mssql_conn: Connection,
) -> None:
    """
    Tests that the environment variables get set correctly.
    """
    profile_mapping = get_automatic_profile_mapping(
        mock_mssql_conn.conn_id,
        profile_args={"schema": "my_schema"},
    )
    assert profile_mapping.env_vars == {
        "COSMOS_CONN_MSSQL_PASSWORD": mock_mssql_conn.password,
    }