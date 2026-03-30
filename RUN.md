# How to Run (Project 3)

## 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional env vars (copy and edit):

```bash
cp configs/.env.example .env
# then export variables in your shell or use a dotenv loader
```

## 2) Run the backend (FastAPI)

```bash
uvicorn integrated_system.app.api:app --reload --port 8000
```

## 3) Run the frontend (Streamlit)

```bash
streamlit run integrated_system/app/app.py
```

## 4) Run evaluation (smoke test)

```bash
python -m integrated_system.evaluation.evaluate_pipeline
```

## (Optional) Rebuild the knowledge base JSON

```bash
python src/data/ingest_kb.py --output-json integrated_system/app/knowledge_base.json
```

## (Optional) Regenerate the architecture diagram

```bash
python scripts/generate_diagram_png.py
```

## 5) One-command reproducibility

```bash
bash reproduce.sh
```

Outputs:
- Logs are written under `logs/` and `integrated_system/logs/`.
