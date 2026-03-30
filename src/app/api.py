"""Rubric-friendly FastAPI entrypoint.

The actual app is `integrated_system.app.api:app`.
"""

from integrated_system.app.api import app

__all__ = ["app"]
