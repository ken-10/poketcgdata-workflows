from __future__ import annotations

from cosmos.profiles import BaseProfileMapping
from typing import Any

"""
Adapted from:
https://github.com/astronomer/astronomer-cosmos/blob/main/cosmos/profiles/postgres/user_pass.py
"""

class SqlServerUserPasswordProfileMapping(BaseProfileMapping):

    airflow_connection_type: str = "mssql"
    dbt_profile_type: str = "sqlserver"

    required_fields = [
        "host",
        "user",
        "password",
        "schema",
        "database",
        "driver"
    ]
    secret_fields = [
        "password",
    ]
    airflow_param_mapping = {
        "host": "host",
        "user": "login",
        "password": "password",
        "port": "port",
        "database": "schema",
        "driver": "driver",
        "keepalives_idle": "extra.keepalives_idle",
        "sslmode": "extra.sslmode",
    }

    @property
    def profile(self) -> dict[str, Any | None]:
        "Gets profile. The password is stored in an environment variable."
        profile = {
            "port": 1433,
            **self.mapped_params,
            **self.profile_args,
            # password should always get set as env var
            "password": self.get_env_var_format("password"),
        }

        return self.filter_null(profile)

    @property
    def mock_profile(self) -> dict[str, Any | None]:
        "Gets mock profile. Defaults port to 1433."
        parent_mock = super().mock_profile

        return {
            "port": 1433,
            **parent_mock,
        }

