from __future__ import annotations

from .config import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_ROLE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE,
)


class SnowflakeService:
    def __init__(self):
        self.configured = all(
            [
                SNOWFLAKE_ACCOUNT,
                SNOWFLAKE_USER,
                SNOWFLAKE_PASSWORD,
                SNOWFLAKE_WAREHOUSE,
                SNOWFLAKE_DATABASE,
                SNOWFLAKE_SCHEMA,
            ]
        )

    def get_region_facts(self, region: str | None) -> list[dict]:
        if self.configured:
            try:
                return self._fetch_live_facts(region)
            except Exception:
                return self._fallback_facts(region, source="snowflake-fallback")
        return self._fallback_facts(region, source="sample-warehouse")

    def _fetch_live_facts(self, region: str | None) -> list[dict]:
        import snowflake.connector

        connection = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE,
        )
        query = """
            SELECT METRIC, VALUE
            FROM DISASTER_FORECAST_METRICS
            WHERE (%(region)s IS NULL OR REGION = %(region)s)
            ORDER BY UPDATED_AT DESC
            LIMIT 5
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, {"region": region})
                rows = cursor.fetchall()
        finally:
            connection.close()

        return [
            {"metric": str(metric), "value": str(value), "source": "snowflake-live"}
            for metric, value in rows
        ]

    def _fallback_facts(self, region: str | None, source: str) -> list[dict]:
        region_label = region or "Coastal District A"
        return [
            {
                "metric": "Region",
                "value": region_label,
                "source": source,
            },
            {
                "metric": "Population exposure",
                "value": "390000 residents in forecast path",
                "source": source,
            },
            {
                "metric": "Shelter readiness",
                "value": "78% of planned shelter capacity available",
                "source": source,
            },
        ]
