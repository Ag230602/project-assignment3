from __future__ import annotations

from .config import TOP_K_RETRIEVAL
from .knowledge_base import KnowledgeBase
from .model_service import ModelService
from .snowflake_service import SnowflakeService


class DisasterForecastAgent:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.model_service = ModelService()
        self.snowflake = SnowflakeService()

    def answer(self, instruction: str, user_input: str, region: str | None, top_k: int | None = None):
        retrieval_count = top_k or TOP_K_RETRIEVAL
        query = f"{instruction}\n{user_input}\n{region or ''}".strip()
        documents = self.knowledge_base.search(query, top_k=retrieval_count)
        facts = self.snowflake.get_region_facts(region)

        reasoning = [
            "Parsed the user request into task instruction, forecast indicators, and optional region.",
            f"Retrieved {len(documents)} supporting knowledge-base documents.",
            f"Collected {len(facts)} structured warehouse facts for grounding.",
            "Synthesized a response prompt for the domain-adapted model.",
        ]

        prompt = self._build_prompt(instruction, user_input, region, documents, facts)
        explanation, used_fallback_model = self.model_service.generate(prompt)
        return {
            "explanation": explanation,
            "retrieved_context": documents,
            "warehouse_facts": facts,
            "reasoning_trace": reasoning,
            "used_fallback_model": used_fallback_model,
        }

    def health(self):
        return {
            "status": "ok",
            "model_ready": self.model_service.ready,
            "knowledge_base_ready": bool(self.knowledge_base.documents),
            "snowflake_configured": self.snowflake.configured,
        }

    def _build_prompt(self, instruction: str, user_input: str, region: str | None, docs: list[dict], facts: list[dict]) -> str:
        context_block = "\n".join(
            [
                f"- {doc['title']} ({doc['source_type']}, score={doc['score']}): {doc['content']}"
                for doc in docs
            ]
        ) or "- No relevant supporting documents found."

        facts_block = "\n".join(
            [f"- {fact['metric']}: {fact['value']} [{fact['source']}]" for fact in facts]
        ) or "- No warehouse facts available."

        region_line = region or "No region supplied"
        return (
            "You are a disaster forecasting AI assistant. Use the retrieved context and structured "
            "warehouse facts to produce a concise, actionable explanation for emergency planners.\n"
            f"Instruction: {instruction}\n"
            f"Forecast Input: {user_input}\n"
            f"Region: {region_line}\n"
            "Retrieved Context:\n"
            f"{context_block}\n"
            "Structured Facts:\n"
            f"{facts_block}\n"
            "Response:"
        )
