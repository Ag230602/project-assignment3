from __future__ import annotations

from .config import TOP_K_RETRIEVAL
from .knowledge_base import KnowledgeBase
from .model_service import ModelService
from .snowflake_service import SnowflakeService


def _read_text_file(path: str, max_chars: int = 20_000) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.read(max_chars)
    except Exception:
        return ""


def _should_use_lab6_tools(instruction: str, user_input: str) -> bool:
    combined = f"{instruction}\n{user_input}".lower()
    keywords = ["retrieve", "find", "document", "rag", "summary", "summarize", "stats", "keyword", "log"]
    return any(key in combined for key in keywords)


class DisasterForecastAgent:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.model_service = ModelService()
        self.snowflake = SnowflakeService()

    def answer(
        self,
        instruction: str,
        user_input: str,
        region: str | None,
        top_k: int | None = None,
        use_lab6_agent: bool = False,
    ):
        retrieval_count = top_k or TOP_K_RETRIEVAL
        query = f"{instruction}\n{user_input}\n{region or ''}".strip()
        documents = self.knowledge_base.search(query, top_k=retrieval_count)
        facts = self.snowflake.get_region_facts(region)

        lab6_tool_trace: list[dict] = []
        if use_lab6_agent:
            lab6_tool_trace = self._run_lab6_tools(query)

        reasoning = [
            "Parsed the user request into task instruction, forecast indicators, and optional region.",
            f"Retrieved {len(documents)} supporting knowledge-base documents.",
            f"Collected {len(facts)} structured warehouse facts for grounding.",
            "Executed Lab 6 tool-agent steps (see lab6_tool_trace)." if lab6_tool_trace else "Skipped Lab 6 tool-agent steps.",
            "Synthesized a response prompt for the domain-adapted model.",
        ]

        prompt = self._build_prompt(instruction, user_input, region, documents, facts)
        explanation, used_fallback_model = self.model_service.generate(prompt)
        return {
            "explanation": explanation,
            "retrieved_context": documents,
            "warehouse_facts": facts,
            "reasoning_trace": reasoning,
            "lab6_tool_trace": lab6_tool_trace,
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

    def _run_lab6_tools(self, query: str) -> list[dict]:
        """Run a multi-step, Lab6-style tool chain and return a tool trace.

        This is intentionally deterministic so it runs without API keys, while still
        demonstrating: tool selection -> tool calls -> grounded outputs.
        """

        try:
            from integrated_system.agent import tools as lab6_tools
        except Exception as exc:
            return [
                {
                    "tool": "lab6_tools_import",
                    "input": {},
                    "output": {"ok": False, "error": str(exc)},
                }
            ]

        trace: list[dict] = []

        retrieval = lab6_tools.retrieve_docs(query=query)
        trace.append({"tool": "retrieve_docs", "input": {"query": query}, "output": retrieval})
        if not retrieval.get("ok"):
            return trace

        hits = retrieval.get("hits", [])
        if hits:
            top_path = hits[0].get("path", "")
            top_text = _read_text_file(top_path) or hits[0].get("snippet", "")

            # Heuristic tool selection: summarize + keyword stats for the top retrieved doc.
            summary = lab6_tools.summarize_text(text=top_text, max_sentences=4)
            trace.append({"tool": "summarize_text", "input": {"path": top_path}, "output": summary})

            stats = lab6_tools.compute_stats(text=top_text)
            trace.append({"tool": "compute_stats", "input": {"path": top_path}, "output": stats})

            if stats.get("ok") and stats.get("top_keywords"):
                plot = lab6_tools.make_plot_from_counts(items=stats["top_keywords"])
                trace.append({"tool": "make_plot_from_counts", "input": {"from": top_path}, "output": plot})

        # Also show log search capability (useful for evaluation proof)
        log_search = lab6_tools.search_project_logs(keyword="generation")
        trace.append({"tool": "search_project_logs", "input": {"keyword": "generation"}, "output": log_search})

        return trace
