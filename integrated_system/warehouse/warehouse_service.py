from __future__ import annotations

"""Snowflake warehouse wrapper for the integrated system.

This module re-exports the SnowflakeService used in the Lab 8/9 app
so that other components can import a stable interface from
integrated_system.warehouse.
"""

from integrated_system.app.ai_app.snowflake_service import SnowflakeService


__all__ = ["SnowflakeService"]
