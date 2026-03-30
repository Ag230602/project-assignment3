#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running smoke test experiment..."
python tests/smoke_test.py

echo "Execution finished. Logs saved in logs/ directory."