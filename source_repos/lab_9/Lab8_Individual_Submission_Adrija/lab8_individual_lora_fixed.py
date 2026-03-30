
"""
lab8_individual_lora_fixed.py

Simplified Lab 8 script for domain adaptation using LoRA.
This version avoids TRL compatibility issues and uses HuggingFace Trainer.

Commands:
    python lab8_individual_lora_fixed.py --build-dataset
    python lab8_individual_lora_fixed.py --train
    python lab8_individual_lora_fixed.py --evaluate
"""

import argparse
import inspect
import json
import os
import torch
from datasets import Dataset
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)

DEFAULT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATASET_PATH = "instruction_dataset.json"
OUTPUT_DIR = "lab8_adapted_model"
EVAL_PATH = "evaluation_results_lab8.json"


def build_dataset():
    examples = []
    for i in range(51, 81):
        examples.append(
            {
                "instruction": "Explain disaster forecast uncertainty for emergency planners.",
                "input": f"Storm probability {i}%, confidence interval ±{i + 10} km, population exposure {100000 + i * 1000}.",
                "output": "The forecast suggests potential impact in nearby regions. Because the uncertainty band is wide, emergency planners should prepare contingency plans and monitor updates.",
            }
        )

    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)

    print(f"Dataset created: {DATASET_PATH} ({len(examples)} examples)")


def load_dataset(tokenizer):
    with open(DATASET_PATH, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for ex in data:
        text = f"Instruction: {ex['instruction']}\nInput: {ex['input']}\nResponse: {ex['output']}"
        tokens = tokenizer(text, truncation=True, padding="max_length", max_length=256)
        tokens["labels"] = tokens["input_ids"].copy()
        rows.append(tokens)

    return Dataset.from_list(rows)


def train():
    tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset(tokenizer)

    model = AutoModelForCausalLM.from_pretrained(
        DEFAULT_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )

    lora_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=1,
        per_device_train_batch_size=1,
        logging_steps=1,
        save_strategy="epoch",
        report_to="none"
    )

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer_kwargs = {
        "model": model,
        "args": args,
        "train_dataset": dataset,
        "data_collator": data_collator,
    }
    trainer_signature = inspect.signature(Trainer.__init__).parameters
    if "tokenizer" in trainer_signature:
        trainer_kwargs["tokenizer"] = tokenizer
    elif "processing_class" in trainer_signature:
        trainer_kwargs["processing_class"] = tokenizer

    trainer = Trainer(**trainer_kwargs)

    trainer.train()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    trainer.model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("Model saved to:", OUTPUT_DIR)


def generate(model, tokenizer, instruction, inp):
    prompt = f"Instruction: {instruction}\nInput: {inp}\nResponse:"
    tokens = tokenizer(prompt, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        device = next(model.parameters()).device
        tokens = {k: v.to(device) for k, v in tokens.items()}
        out = model.generate(**tokens, max_new_tokens=100, do_sample=False)

    decoded = tokenizer.decode(out[0], skip_special_tokens=True)
    if "Response:" in decoded:
        return decoded.split("Response:", 1)[-1].strip()
    return decoded.strip()


def evaluate():
    if not os.path.exists(OUTPUT_DIR):
        raise FileNotFoundError("Run training first")

    tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    base_model = AutoModelForCausalLM.from_pretrained(
        DEFAULT_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    
    adapted_base = AutoModelForCausalLM.from_pretrained(
        DEFAULT_MODEL,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    adapted_model = PeftModel.from_pretrained(adapted_base, OUTPUT_DIR)

    queries = [
        (1, "Explain hurricane forecast uncertainty for emergency planners.", "Storm probability 74%, confidence interval ±85 km, coastal population exposure 390000."),
        (2, "Generate a humanitarian impact explanation from forecast indicators.", "Cyclone probability 79%, displacement risk high, child exposure 110000, water access fragile."),
        (3, "Interpret uncertainty for flood response planning.", "River crest 2.4–3.1 m above normal, levee performance uncertain, mobile home parks exposed."),
        (4, "Explain low confidence but high consequence forecast conditions.", "Impact probability 43%, airport exposure high, major hospital nearby, road access limited."),
        (5, "Explain how uncertainty affects evacuation planning.", "Primary zone likely, adjacent zone possible, transport capacity low, road congestion expected."),
        (6, "Create a concise hazard briefing for emergency managers.", "48-hour impact probability 81%, rainfall 195 mm, school exposure high, shelter readiness medium."),
        (7, "Translate forecast outputs into a public-safety explanation.", "Wind gusts 80 mph, outage risk high, elderly residents 47000, tree-fall risk moderate."),
        (8, "Use a historical analog to explain present storm risk.", "Track resembles Ida, drainage limitations present, urban flood risk high."),
        (9, "Explain resource allocation needs from a hazard forecast.", "Storm probability 69%, hospitals near capacity, shelters not fully staffed, bridge closure risk moderate."),
        (10, "Write a compact disaster briefing from structured indicators.", "Probability 70%, confidence medium, rainfall 175 mm, power grid vulnerability high."),
    ]

    results = []

    for query_id, instruction, model_input in queries:
        baseline = generate(base_model, tokenizer, instruction, model_input)
        adapted = generate(adapted_model, tokenizer, instruction, model_input)

        results.append({
            "query_id": query_id,
            "instruction": instruction,
            "input": model_input,
            "baseline_response": baseline,
            "adapted_response": adapted,
            "reviewer_notes": "",
            "baseline_score_relevance": "",
            "adapted_score_relevance": "",
            "baseline_score_domain_specificity": "",
            "adapted_score_domain_specificity": "",
            "baseline_score_decision_usefulness": "",
            "adapted_score_decision_usefulness": "",
        })

    with open(EVAL_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Evaluation saved to:", EVAL_PATH)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dataset", action="store_true")
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    args = parser.parse_args()

    if args.build_dataset:
        build_dataset()

    if args.train:
        train()

    if args.evaluate:
        evaluate()


if __name__ == "__main__":
    main()
