# Disaster Forecast AI Application

This project is a GitHub-ready starter AI application for disaster forecasting and emergency planning. It includes:

- Data Sources
- Knowledge Base
- Retrieval Pipeline
- Domain-Adapted Model
- AI Agent Reasoning
- Snowflake Data Warehouse integration scaffold
- Application Interface
- Monitoring and Deployment starter endpoints

## Submission Type

This folder is prepared as an individual submission, not a group submission.

Submission-support files included:

- `individual_report.txt`
- `Individual_Contribution_Report.pdf`
- `github_link.md`
- `GitHub_Contribution_Evidence.md`
- `Individual_Submission_Checklist.md`

## Project Structure

```text
.
|-- ai_app/
|   |-- agent.py
|   |-- config.py
|   |-- knowledge_base.py
|   |-- model_service.py
|   |-- models.py
|   `-- snowflake_service.py
|-- api.py
|-- app.py
|-- knowledge_base.json
|-- requirements.txt
`-- lab8_adapted_model/
```

## Features

- FastAPI backend with `/generate`, `/health`, and `/architecture`
- Streamlit interface for end users
- Local knowledge-base retrieval for grounded responses
- Snowflake-ready warehouse service with safe sample fallback
- Domain-adapted LoRA model support
- Graceful fallback when the base model is not available locally
- Request logging, metrics, and lightweight evaluation endpoints

## Application Workflow

1. The user enters a planning request in the Streamlit interface.
2. The backend retrieval pipeline searches `knowledge_base.json`.
3. The agent gathers structured facts from Snowflake or a sample warehouse fallback.
4. The grounded prompt is assembled for the adapted model.
5. The response, retrieved documents, warehouse facts, and reasoning trace are returned to the UI.

## System Evaluation And Monitoring

- `GET /health` checks overall service readiness
- `GET /metrics` reports uptime, request volume, errors, fallback usage, and latency
- `GET /evaluation` runs a lightweight multi-scenario pipeline evaluation

These endpoints help demonstrate system evaluation and continuous monitoring for the submission.

## Logging And Debugging Support

- Rotating logs are written to `logs/application.log`
- Each request receives a request ID in the backend middleware
- Errors are captured in monitoring summaries and application logs
- The UI includes buttons to inspect health, metrics, and evaluation output

## Deployment And System Stability

- The backend is deployable with `uvicorn api:app --reload`
- The frontend is deployable with `streamlit run app.py`
- If Snowflake is not configured, the system falls back to sample facts
- If the base model is unavailable locally, the system falls back to a grounded response instead of crashing
- This makes the application stable enough to demo in restricted environments

## Setup

```bash
pip install -r requirements.txt
```

Optional environment variables can be copied from `.env.example`.

## Run

Backend:

```bash
uvicorn api:app --reload
```

Frontend:

```bash
https://cqbvrfmxw86jpcb9qw5bhg.streamlit.app/
```

When running the frontend in a deployed environment, set `API_URL` to your public backend URL (for example `https://disaster-forecast-api.onrender.com`) instead of `localhost`.

## Notes On The Model

The repository includes the LoRA adapter artifacts in `lab8_adapted_model/`. To run full model generation locally, set `LOCAL_BASE_MODEL_PATH` to a downloaded compatible base model directory. If no local base model is available, the app still works and returns a grounded fallback answer using retrieval plus warehouse facts.

## Snowflake Configuration

Set these variables to enable live Snowflake queries:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_ROLE`

## Health Check

```bash
curl http://localhost:8000/health
```

This reports whether:

- the model is ready
- the knowledge base is loaded
- Snowflake is configured

Additional endpoints:

- `http://localhost:8000/metrics`
- `http://localhost:8000/evaluation`

## GitHub Push

After reviewing your files:

```bash
git add .
git commit -m "Build disaster forecast AI application"
git push
```

## Deployment

This repository includes `render.yaml` and `DEPLOYMENT.md` so you can deploy both the FastAPI backend and the Streamlit frontend from GitHub using Render.

As an alternative, use `RAILWAY_DEPLOYMENT.md` for deploying the same two-service setup on Railway.
