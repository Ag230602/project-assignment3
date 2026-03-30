from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    instruction: str
    input: str
    region: Optional[str] = None
    top_k: int = Field(default=3, ge=1, le=10)
    use_lab6_agent: bool = False


class SourceDocument(BaseModel):
    title: str
    content: str
    source_type: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class WarehouseFact(BaseModel):
    metric: str
    value: str
    source: str


class QueryResponse(BaseModel):
    explanation: str
    retrieved_context: list[SourceDocument] = Field(default_factory=list)
    warehouse_facts: list[WarehouseFact] = Field(default_factory=list)
    reasoning_trace: list[str] = Field(default_factory=list)
    lab6_tool_trace: list[dict[str, Any]] = Field(default_factory=list)
    used_fallback_model: bool = False


class HealthResponse(BaseModel):
    status: str
    model_ready: bool
    knowledge_base_ready: bool
    snowflake_configured: bool
