#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Installing dependencies..."
pip install -r requirements.txt

mkdir -p logs

echo "Running integrated evaluation smoke test..."
python -m integrated_system.evaluation.evaluate_pipeline | tee "logs/reproduce_evaluate_pipeline.log"

echo "Execution finished. Logs saved in logs/ directory."