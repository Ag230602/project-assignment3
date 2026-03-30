
"""
lab8_individual_lora.py

Individual Lab 8 script for CS 5542:
- builds a small instruction dataset (20–50 examples)
- formats examples for supervised fine-tuning
- applies LoRA-based domain adaptation
- saves the adapted model
- runs a simple baseline vs adapted evaluation

Author: Adrija Ghosh
Project: GenAI-Driven Uncertainty-Aware Forecasting and Recovery Simulation for Decision Support

Recommended usage:
    pip install torch transformers datasets peft trl accelerate
    python lab8_individual_lora.py --build-dataset
    python lab8_individual_lora.py --train
    python lab8_individual_lora.py --evaluate
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Dict, List

import torch
from datasets import Dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
)
from trl import SFTTrainer


DEFAULT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATASET_PATH = "instruction_dataset_lab8.json"
OUTPUT_DIR = "lab8_adapted_model"
EVAL_PATH = "evaluation_results_lab8.json"


@dataclass
class Example:
    instruction: str
    input: str
    output: str


def build_instruction_examples() -> List[Dict[str, str]]:
    """Create a small instruction dataset aligned with the Lab 8 guideline size."""
    examples = [
        Example(
            instruction="Explain hurricane forecast uncertainty for emergency planners.",
            input="Storm probability 68%, confidence interval ±90 km, expected landfall within 36 hours, population exposure 420000.",
            output="The storm has a moderately high chance of affecting the projected coastal zone. Because the uncertainty band is wide, nearby districts outside the main track should also prepare evacuation and shelter plans."
        ),
        Example(
            instruction="Generate a decision-support explanation from forecast and exposure data.",
            input="Rainfall forecast 220 mm in 24 hours, flash-flood risk high, low-income households in floodplain 18000.",
            output="The forecast indicates severe flooding potential over the next day. Response teams should prioritize floodplain communities, especially low-income households that may have limited evacuation resources."
        ),
        Example(
            instruction="Summarize the practical meaning of a wide uncertainty band in a storm forecast.",
            input="Track spread 140 km, wind speed estimate 95–115 mph, coastal infrastructure exposure moderate.",
            output="A wide uncertainty band means the storm could shift enough to affect areas outside the most likely track. Planners should avoid focusing on one city alone and prepare neighboring infrastructure for possible impact."
        ),
        Example(
            instruction="Explain a best-case storm scenario using forecast data.",
            input="Landfall probability 35%, weakening before coast, rainfall 40–80 mm, surge risk low.",
            output="In the best-case scenario, the storm weakens before reaching shore and produces manageable rainfall with limited coastal flooding. Preparedness should continue, but large-scale evacuation may not be necessary."
        ),
        Example(
            instruction="Explain a worst-case storm scenario using forecast data.",
            input="Landfall probability 72%, rainfall above 250 mm, storm surge 2.8 m, hospital exposure high.",
            output="In the worst-case scenario, the storm reaches the coast with major rainfall and dangerous surge. Hospitals and nearby transport routes should be protected immediately because service disruption could affect emergency care."
        ),
        Example(
            instruction="Compare forecast confidence across two regions.",
            input="Region A probability 75%, spread ±40 km. Region B probability 60%, spread ±120 km.",
            output="Region A has both higher impact probability and tighter forecast confidence, so planning there can be more targeted. Region B still requires preparation because the lower confidence means the impact area is less certain and may shift."
        ),
        Example(
            instruction="Translate forecast outputs into a public-safety explanation.",
            input="Wind gusts 70 mph, tree-fall risk moderate, power outage risk high, elderly population 52000.",
            output="Strong winds may cause falling trees and widespread power interruptions. Emergency communication should focus on elderly residents who may be especially vulnerable during prolonged outages."
        ),
        Example(
            instruction="Use a historical analog to explain present storm risk.",
            input="Current track resembles Hurricane Ida, rainfall anomaly high, urban drainage capacity low.",
            output="Because the projected pattern resembles Hurricane Ida and current drainage capacity is limited, the area may face rapid urban flooding. Officials should prepare for both transport disruption and neighborhood-level rescue needs."
        ),
        Example(
            instruction="Explain uncertainty-aware response priorities.",
            input="Storm probability 58%, surge uncertainty moderate, bridge exposure high, shelters available 6.",
            output="Even though the storm path is not fully certain, bridge exposure and limited shelter capacity make early coordination important. Transportation access and shelter allocation should be prioritized now rather than waiting for certainty."
        ),
        Example(
            instruction="Create a concise hazard briefing for emergency managers.",
            input="48-hour forecast: 80% coastal impact, rainfall 180 mm, schools in risk zone 22, evacuation readiness medium.",
            output="There is a high likelihood of coastal impact within 48 hours. Heavy rainfall and exposure of 22 schools justify early protective action and coordination with transportation and shelter teams."
        ),
        Example(
            instruction="Explain why probabilistic forecasts matter for planning.",
            input="Probability cone covers three counties, most likely track central county, outer counties lower probability.",
            output="Probabilistic forecasts help planners prepare beyond the single most likely track. Even outer counties with lower probability may still experience serious effects and should not be excluded from readiness actions."
        ),
        Example(
            instruction="Generate an explanation focused on vulnerable populations.",
            input="Heatwave probability 84%, low-income elderly population 27000, cooling center access limited.",
            output="The forecast indicates a strong chance of severe heat impacts. Because vulnerable elderly residents have limited access to cooling centers, outreach and transport support should be expanded immediately."
        ),
        Example(
            instruction="Interpret uncertainty for flood response planning.",
            input="River crest expected 2.1–3.0 m above normal, levee condition uncertain, mobile homes exposed 900.",
            output="Flood severity may range from serious to extreme depending on the river crest and levee performance. Mobile home communities should be prioritized because even moderate increases in water level could create life-threatening conditions."
        ),
        Example(
            instruction="Explain low confidence but high consequence forecast conditions.",
            input="Storm probability 42%, surge risk uncertain, airport exposure high, fuel depot nearby.",
            output="Although forecast confidence is not high, the exposed airport and nearby fuel depot raise the consequences of under-preparation. Low confidence does not mean low risk when critical assets are involved."
        ),
        Example(
            instruction="Generate a humanitarian impact explanation from forecast indicators.",
            input="Cyclone probability 77%, displacement risk high, clean water access fragile, children exposed 130000.",
            output="The projected cyclone could create major humanitarian needs, especially for children in areas with fragile water access. Preparedness should include shelter, safe water planning, and rapid post-impact assessment."
        ),
        Example(
            instruction="Describe how uncertainty should be communicated to decision-makers.",
            input="Forecast confidence medium, alternate inland track possible, rainfall range 100–240 mm.",
            output="Decision-makers should be told both the most likely outcome and the credible alternate track. The large rainfall range means inland flooding remains possible even if the main coastal scenario weakens."
        ),
        Example(
            instruction="Explain resource allocation needs from a hazard forecast.",
            input="Impact probability 71%, hospital beds limited, road closure likelihood high, shelters partially staffed.",
            output="Resources should be positioned before road closures begin. Limited hospital capacity and partially staffed shelters mean response effectiveness will depend on early personnel and supply movement."
        ),
        Example(
            instruction="Summarize forecast-driven school safety concerns.",
            input="Tornado probability moderate, school buses active during warning window, shelter readiness uneven.",
            output="Because school transport overlaps with the warning window, student safety planning requires immediate coordination. Shelter readiness should be confirmed before dismissal or route decisions are made."
        ),
        Example(
            instruction="Generate a short adaptation-aware answer for a disaster assistant.",
            input="Storm surge 1.9–2.6 m, nursing homes in surge zone 4, confidence moderate.",
            output="Moderate confidence and significant surge depth indicate that nursing homes in the surge zone need early protection or relocation planning. Waiting for a narrower forecast could reduce safe response time."
        ),
        Example(
            instruction="Explain why retrieved historical events improve the answer.",
            input="Current flood pattern resembles 2019 Missouri flooding; levee overtopping was reported in similar areas.",
            output="Historical comparisons improve confidence in the explanation because they show how similar conditions affected the same type of infrastructure before. This makes the response more actionable than a generic forecast summary."
        ),
        Example(
            instruction="Create a clear response for a dashboard user comparing baseline and adapted reasoning.",
            input="Baseline says 'storm likely soon'. Forecast data show 76% impact probability, 210 mm rainfall, child exposure high.",
            output="A stronger domain-adapted response should state that there is a high likelihood of storm impact, that heavy rainfall could create severe flooding, and that areas with high child exposure should be prioritized in preparedness actions."
        ),
        Example(
            instruction="Produce an explanation of forecast calibration in simple terms.",
            input="Observed impacts matched 7 of 10 previous forecasts at this probability level.",
            output="This forecast probability level has performed reasonably well in past events, which means planners can treat it as useful but not certain. Preparedness should be proportionate to both the probability and the consequences."
        ),
        Example(
            instruction="Interpret a forecast where confidence improves over time.",
            input="72-hour spread ±180 km, 24-hour spread ±60 km, exposure rising near coast.",
            output="The forecast becomes more precise closer to impact, but waiting for full certainty may leave too little time to act. Because coastal exposure is rising, staged preparation should begin now and intensify as confidence improves."
        ),
        Example(
            instruction="Explain how uncertainty affects evacuation planning.",
            input="Evacuation zone A likely, zone B possible, road bottleneck risk high, public transport limited.",
            output="Uncertainty means evacuation decisions should account for both likely and possible zones. With road bottlenecks and limited public transport, phased evacuation planning is safer than waiting for a final narrow track."
        ),
        Example(
            instruction="Write a compact disaster briefing from structured indicators.",
            input="Probability 69%, confidence medium, rainfall 160 mm, shelters 80% ready, hospitals low backup power.",
            output="The area faces a meaningful storm threat with heavy rainfall and moderate forecast confidence. Shelter preparation is progressing, but hospitals with weak backup power require immediate attention."
        ),
    ]
    return [e.__dict__ for e in examples]


def save_dataset(path: str = DATASET_PATH) -> None:
    examples = build_instruction_examples()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(examples)} examples to {path}")


def format_example(example: Dict[str, str]) -> Dict[str, str]:
    text = (
        f"### Instruction:\n{example['instruction']}\n\n"
        f"### Input:\n{example['input']}\n\n"
        f"### Response:\n{example['output']}"
    )
    return {"text": text}


def load_training_dataset(path: str = DATASET_PATH) -> Dataset:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    formatted = [format_example(x) for x in raw]
    return Dataset.from_list(formatted)


def load_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_base_model(model_name: str):
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map="auto" if torch.cuda.is_available() else None
    )
    return model


def train(model_name: str = DEFAULT_MODEL, dataset_path: str = DATASET_PATH, output_dir: str = OUTPUT_DIR):
    dataset = load_training_dataset(dataset_path)
    tokenizer = load_tokenizer(model_name)
    model = load_base_model(model_name)

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"] if "llama" in model_name.lower() or "tinyllama" in model_name.lower() else None,
    )

    model = get_peft_model(model, peft_config)

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        num_train_epochs=2,
        logging_steps=5,
        save_strategy="epoch",
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=512,
        args=training_args,
    )

    trainer.train()
    trainer.model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Adapted model saved to: {output_dir}")


def generate_response(model, tokenizer, instruction: str, model_input: str, max_new_tokens: int = 160) -> str:
    prompt = (
        f"### Instruction:\n{instruction}\n\n"
        f"### Input:\n{model_input}\n\n"
        f"### Response:\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.3,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("### Response:\n", 1)[-1].strip()


def get_eval_queries() -> List[Dict[str, str]]:
    return [
        {
            "instruction": "Explain hurricane forecast uncertainty for emergency planners.",
            "input": "Storm probability 74%, confidence interval ±85 km, coastal population exposure 390000.",
        },
        {
            "instruction": "Generate a humanitarian impact explanation from forecast indicators.",
            "input": "Cyclone probability 79%, displacement risk high, child exposure 110000, water access fragile.",
        },
        {
            "instruction": "Interpret uncertainty for flood response planning.",
            "input": "River crest 2.4–3.1 m above normal, levee performance uncertain, mobile home parks exposed.",
        },
        {
            "instruction": "Explain low confidence but high consequence forecast conditions.",
            "input": "Impact probability 43%, airport exposure high, major hospital nearby, road access limited.",
        },
        {
            "instruction": "Explain how uncertainty affects evacuation planning.",
            "input": "Primary zone likely, adjacent zone possible, transport capacity low, road congestion expected.",
        },
        {
            "instruction": "Create a concise hazard briefing for emergency managers.",
            "input": "48-hour impact probability 81%, rainfall 195 mm, school exposure high, shelter readiness medium.",
        },
        {
            "instruction": "Translate forecast outputs into a public-safety explanation.",
            "input": "Wind gusts 80 mph, outage risk high, elderly residents 47000, tree-fall risk moderate.",
        },
        {
            "instruction": "Use a historical analog to explain present storm risk.",
            "input": "Track resembles Ida, drainage limitations present, urban flood risk high.",
        },
        {
            "instruction": "Explain resource allocation needs from a hazard forecast.",
            "input": "Storm probability 69%, hospitals near capacity, shelters not fully staffed, bridge closure risk moderate.",
        },
        {
            "instruction": "Write a compact disaster briefing from structured indicators.",
            "input": "Probability 70%, confidence medium, rainfall 175 mm, power grid vulnerability high.",
        },
    ]


def evaluate(model_name: str = DEFAULT_MODEL, adapted_dir: str = OUTPUT_DIR, output_path: str = EVAL_PATH):
    tokenizer = load_tokenizer(model_name)
    baseline_model = load_base_model(model_name)

    adapted_base = load_base_model(model_name)
    adapted_model = PeftModel.from_pretrained(adapted_base, adapted_dir)

    results = []
    for i, q in enumerate(get_eval_queries(), start=1):
        baseline = generate_response(baseline_model, tokenizer, q["instruction"], q["input"])
        adapted = generate_response(adapted_model, tokenizer, q["instruction"], q["input"])
        results.append(
            {
                "query_id": i,
                "instruction": q["instruction"],
                "input": q["input"],
                "baseline_response": baseline,
                "adapted_response": adapted,
            }
        )
        print(f"Finished evaluation query {i}/10")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Saved evaluation results to {output_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Lab 8 individual LoRA fine-tuning script")
    parser.add_argument("--build-dataset", action="store_true", help="Create the 20–50 example instruction dataset")
    parser.add_argument("--train", action="store_true", help="Train a LoRA-adapted model")
    parser.add_argument("--evaluate", action="store_true", help="Run baseline vs adapted evaluation")
    parser.add_argument("--model-name", type=str, default=DEFAULT_MODEL, help="Base model to use")
    parser.add_argument("--dataset-path", type=str, default=DATASET_PATH, help="Path to instruction dataset JSON")
    parser.add_argument("--output-dir", type=str, default=OUTPUT_DIR, help="Directory to save adapted model")
    parser.add_argument("--eval-path", type=str, default=EVAL_PATH, help="Path to save evaluation JSON")
    return parser.parse_args()


def main():
    args = parse_args()

    if not (args.build_dataset or args.train or args.evaluate):
        print("No action selected. Use one or more of: --build-dataset --train --evaluate")
        return

    if args.build_dataset:
        save_dataset(args.dataset_path)

    if args.train:
        if not os.path.exists(args.dataset_path):
            raise FileNotFoundError(
                f"Dataset not found at {args.dataset_path}. Run with --build-dataset first."
            )
        train(args.model_name, args.dataset_path, args.output_dir)

    if args.evaluate:
        if not os.path.exists(args.output_dir):
            raise FileNotFoundError(
                f"Adapted model directory not found at {args.output_dir}. Run with --train first."
            )
        evaluate(args.model_name, args.output_dir, args.eval_path)


if __name__ == "__main__":
    main()
