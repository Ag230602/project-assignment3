from __future__ import annotations

from .agent import DisasterForecastAgent


def run_sample_evaluation(agent: DisasterForecastAgent) -> dict:
    scenarios = [
        {
            "instruction": "Explain hurricane forecast uncertainty for emergency planners.",
            "input": "Storm probability 74%, confidence interval 85 km, coastal population exposure 390000.",
            "region": "Gulf Coast",
        },
        {
            "instruction": "Interpret uncertainty for flood response planning.",
            "input": "River crest 2.4 to 3.1 m above normal, levee performance uncertain, mobile home parks exposed.",
            "region": "Delta Basin",
        },
        {
            "instruction": "Generate a humanitarian impact explanation from forecast indicators.",
            "input": "Cyclone probability 79%, displacement risk high, child exposure 110000, water access fragile.",
            "region": "Coastal District A",
        },
    ]

    results = []
    for scenario in scenarios:
        response = agent.answer(
            instruction=scenario["instruction"],
            user_input=scenario["input"],
            region=scenario["region"],
            top_k=3,
        )
        results.append(
            {
                "scenario": scenario,
                "used_fallback_model": response["used_fallback_model"],
                "retrieved_documents": len(response["retrieved_context"]),
                "warehouse_facts": len(response["warehouse_facts"]),
                "reasoning_steps": len(response["reasoning_trace"]),
            }
        )

    return {
        "scenario_count": len(results),
        "results": results,
        "notes": [
            "This lightweight evaluation checks that retrieval, reasoning, and warehouse grounding complete successfully.",
            "For production evaluation, add human scoring for relevance, factuality, and decision usefulness.",
        ],
    }
