# Reproducibility Notes

Python version:
- Recommend: Python 3.10 or 3.11

Dependencies:
- Install from integrated_system/config/requirements.txt

Environment variables (set via .env or shell):
- SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD
- SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA, SNOWFLAKE_ROLE
- DEFAULT_MODEL (optional, overrides base chat model)
- LOCAL_BASE_MODEL_PATH (optional, path to local HF model)
- KNOWLEDGE_BASE_PATH (optional, defaults to integrated_system/app/knowledge_base.json)

Smoke test command:
- From the project root:
	- bash scripts/reproduce.sh

Run backend (FastAPI):
- uvicorn integrated_system.app.api:app --reload

Run frontend (Streamlit):
- streamlit run integrated_system/app/app.py

Run evaluation:
- python -m integrated_system.evaluation.evaluate_pipeline

Datasets / model artifacts:
- knowledge_base.json already included under integrated_system/app/
- LoRA / adapted model weights under integrated_system/domain_adaptation/lab8_adapted_model/
