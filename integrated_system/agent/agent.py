from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple, Callable

from .tool_schemas import tool_schemas
from . import tools


SYSTEM_PROMPT = (
    "You are an AI agent for a course project. "
    "You MUST use the available tools when helpful, and produce grounded responses. "
    "If you use retrieved documents, cite them by file path. "
    "When tools return errors, explain clearly and continue with alternatives."
)


TOOL_REGISTRY: Dict[str, Callable[..., Dict[str, Any]]] = {
    "retrieve_docs": tools.retrieve_docs,
    "summarize_text": tools.summarize_text,
    "compute_stats": tools.compute_stats,
    "make_plot_from_counts": tools.make_plot_from_counts,
    "search_project_logs": tools.search_project_logs,
}


def _log(line: str, log_path: str = "integrated_system/logs/lab6_agent_execution_log.txt") -> None:
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def run_agent(user_message: str, model: str = "gpt-4.1-mini", max_turns: int = 8) -> Dict[str, Any]:
    """Run the agent with OpenAI tool-calling if OPENAI_API_KEY is set.
    Falls back to a deterministic router if no key is provided (so the app runs).
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _run_fallback_agent(user_message)

    # OpenAI tool calling (Responses API)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        return {"ok": False, "error": f"OpenAI client init failed: {e}", "mode": "openai_init_error"}

    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    tool_calls_total = 0
    start = time.time()

    for turn in range(max_turns):
        _log(f"[TURN {turn}] user={user_message}")

        resp = client.responses.create(
            model=model,
            input=messages,
            tools=tool_schemas,
        )

        # Collect tool calls
        tool_calls = [item for item in resp.output if getattr(item, "type", None) == "tool_call"]
        final_text = "".join([item.text for item in resp.output if getattr(item, "type", None) == "output_text"])

        if tool_calls:
            for tc in tool_calls:
                tool_calls_total += 1
                name = tc.name
                args = tc.arguments
                try:
                    parsed = json.loads(args) if isinstance(args, str) else args
                except Exception:
                    parsed = {}

                _log(f"  tool_call: {name} args={parsed}")

                fn = TOOL_REGISTRY.get(name)
                if not fn:
                    tool_out = {"ok": False, "error": f"Unknown tool: {name}"}
                else:
                    try:
                        tool_out = fn(**parsed)
                    except Exception as e:
                        tool_out = {"ok": False, "error": str(e)}

                _log(f"  tool_result: {name} -> {str(tool_out)[:500]}")

                # Send tool output back to model
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(tool_out)
                })

            continue

        # No tool calls => final
        latency = time.time() - start
        return {
            "ok": True,
            "answer": final_text.strip() or "(No text returned.)",
            "mode": "openai_tool_calling",
            "tool_calls": tool_calls_total,
            "latency_sec": round(latency, 3),
        }

    latency = time.time() - start
    return {
        "ok": True,
        "answer": "Reached max turns without a final response. Check logs for details.",
        "mode": "openai_tool_calling",
        "tool_calls": tool_calls_total,
        "latency_sec": round(latency, 3),
    }


def _run_fallback_agent(user_message: str) -> Dict[str, Any]:
    """Fallback agent that routes to tools without an LLM.
    This is ONLY to keep the Streamlit app runnable without API keys.
    """
    start = time.time()
    _log("[FALLBACK] No OPENAI_API_KEY detected. Using rule-based routing.")

    msg = user_message.lower()

    if "retrieve" in msg or "find" in msg or "document" in msg or "rag" in msg:
        out = tools.retrieve_docs(user_message)
        if out.get("ok"):
            cites = "\n".join([f"- {h['path']} (score={h['score']:.3f})" for h in out["hits"]])
            return {
                "ok": True,
                "answer": "Top matches:\n" + cites + "\n\nTip: Set OPENAI_API_KEY for full tool-calling agent.",
                "mode": "fallback",
                "latency_sec": round(time.time() - start, 3)
            }
        return {"ok": False, "error": out.get("error", "Unknown error"), "mode": "fallback"}

    if "summary" in msg or "summarize" in msg:
        hit = tools.retrieve_docs(user_message, top_k=1)
        if hit.get("ok") and hit["hits"]:
            path = hit["hits"][0]["path"]
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
            except Exception:
                txt = hit["hits"][0]["snippet"]
            summ = tools.summarize_text(txt)
            return {"ok": True, "answer": f"Summary (from {path}):\n{summ.get('summary','')}", "mode": "fallback"}

    if "keyword" in msg or "stats" in msg or "analy" in msg:
        hit = tools.retrieve_docs(user_message, top_k=1)
        if hit.get("ok") and hit["hits"]:
            path = hit["hits"][0]["path"]
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            stats = tools.compute_stats(txt)
            return {"ok": True, "answer": f"Stats (from {path}):\n{json.dumps(stats, indent=2)}", "mode": "fallback"}

    return {
        "ok": True,
        "answer": (
            "Fallback mode is active (no OPENAI_API_KEY).\n"
            "Set OPENAI_API_KEY to enable full agent tool-calling.\n"
            "Meanwhile you can ask: 'retrieve docs about X' or 'summarize X'."
        ),
        "mode": "fallback",
        "latency_sec": round(time.time() - start, 3)
    }
