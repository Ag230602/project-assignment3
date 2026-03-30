How to Reproduce the Experiment

1. Install dependencies
pip install -r requirements.txt

2. Prepare dataset
dataset/mydata/mydata.csv

3. Run pipeline
bash reproduce.sh

4. Verify results
Check logs/ and artifacts/ directories.

Smoke Test
python tests/smoke_test.py
Expected output: Smoke test successful