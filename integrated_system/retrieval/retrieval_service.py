from __future__ import annotations

"""Thin retrieval wrapper for the integrated system.

This module exposes a KnowledgeBase-backed retrieval service so that
other parts of the integrated_system can depend on a stable interface
instead of importing from the app package directly.
"""

from integrated_system.app.ai_app.knowledge_base import KnowledgeBase


class RetrievalService:
    """Simple wrapper around the Lab 8/9 KnowledgeBase search API."""

    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Return top_k documents for a free-text query.

        This delegates to the KnowledgeBase.search method, which
        currently implements a lightweight lexical similarity search.
        """

        return self.knowledge_base.search(query=query, top_k=top_k)
