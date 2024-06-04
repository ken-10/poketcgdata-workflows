"Contains a function to get the profile mapping based on the connection ID."

from __future__ import annotations

from typing import Any, Type

from .SqlServerUserPasswordProfileMapping import SqlServerUserPasswordProfileMapping

from cosmos.profiles.base import BaseProfileMapping


profile_mappings: list[Type[BaseProfileMapping]] = [
    SqlServerUserPasswordProfileMapping
]


def get_automatic_profile_mapping(
    conn_id: str,
    profile_args: dict[str, Any] | None = None,
) -> BaseProfileMapping:
    """
    Returns a profile mapping object based on the connection ID.
    """
    if not profile_args:
        profile_args = {}

    for profile_mapping in profile_mappings:
        mapping = profile_mapping(conn_id, profile_args)
        if mapping.can_claim_connection():
            return mapping

    raise ValueError(f"Could not find a profile mapping for connection {conn_id}.")


__all__ = [
    "BaseProfileMapping",
    "SqlServerUserPasswordProfileMapping"
]
