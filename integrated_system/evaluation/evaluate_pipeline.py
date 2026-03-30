from __future__ import annotations

"""Lightweight evaluation entrypoint for the integrated system.

This reuses the Lab 8/9 sample evaluation to exercise the end-to-end
pipeline (retrieval, agent, warehouse grounding, and model).
"""

from integrated_system.app.ai_app.agent import DisasterForecastAgent
from integrated_system.app.ai_app.evaluation import run_sample_evaluation


def main() -> None:
    agent = DisasterForecastAgent()
    report = run_sample_evaluation(agent)
    print("Scenario count:", report["scenario_count"])
    for idx, result in enumerate(report["results"], start=1):
        scenario = result["scenario"]
        print("\n=== Scenario", idx, "===")
        print("Instruction:", scenario["instruction"])
        print("Region:", scenario["region"])
        print("Used fallback model:", result["used_fallback_model"])
        print("Retrieved documents:", result["retrieved_documents"])
        print("Warehouse facts:", result["warehouse_facts"])
        print("Reasoning steps:", result["reasoning_steps"])


if __name__ == "__main__":
    main()
