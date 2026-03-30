# Individual Contribution Report (Individual Submission)

## Name
Adrija Ghosh

## Repository link
https://github.com/Ag230602/project-assignment3

## One-line system summary
One integrated GenAI system that connects: Data → Knowledge Base → Retrieval (RAG) → Domain-Adapted Model → Tool-using Agent → Snowflake (live or fallback facts) → FastAPI + Streamlit App → Evaluation + Logs → Reproducibility.

## Architecture (diagram + pipeline)
- Architecture diagram image: [diagram.png](diagram.png)
- Architecture notes (Mermaid): [docs/SYSTEM_ARCHITECTURE.md](docs/SYSTEM_ARCHITECTURE.md)

## What is in this folder (structure + purpose)

### “Start here” docs
- Submission guide (links to everything): [PROJECT3_SUBMISSION_GUIDE.md](PROJECT3_SUBMISSION_GUIDE.md)
- Run commands: [RUN.md](RUN.md)
- Reproducibility notes: [docs/reproducibility_notes.md](docs/reproducibility_notes.md)

### Full working integrated system (the real implementation)
- Main package root: [integrated_system/](integrated_system/)
	- App (FastAPI + Streamlit): [integrated_system/app/](integrated_system/app/)
	- Retrieval wrapper: [integrated_system/retrieval/](integrated_system/retrieval/)
	- Domain adaptation artifacts (Lab 8): [integrated_system/domain_adaptation/](integrated_system/domain_adaptation/)
	- Snowflake/warehouse wrapper: [integrated_system/warehouse/](integrated_system/warehouse/)
	- Integrated evaluation: [integrated_system/evaluation/](integrated_system/evaluation/)
	- Logs (agent + experiments): [integrated_system/logs/](integrated_system/logs/)

### Rubric-friendly expected layout (thin wrappers)
Some rubrics expect `src/`, `evaluation/`, `logs/`, and `configs/` at repo root.
- Rubric-friendly wrappers: [src/](src/)
- Root evaluation wrapper: [evaluation/](evaluation/)
- Root logs folder: [logs/](logs/)
- Environment template: [configs/.env.example](configs/.env.example)

### Evidence and reporting artifacts
- Lab 6 evidence reports: [docs/evidence/](docs/evidence/)
- Project report template: [reports/PROJECT3_REPORT_TEMPLATE.md](reports/PROJECT3_REPORT_TEMPLATE.md)
- Contribution table (individual = 100%): [reports/CONTRIBUTION_TABLE.csv](reports/CONTRIBUTION_TABLE.csv)

### Upstream lab repositories (for traceability)
- Source repos snapshot: [source_repos/](source_repos/)
- Merge provenance map: [MERGE_MAP.md](MERGE_MAP.md)

## What I implemented / integrated (my work)

### Lab 6 (Agent + tools) — made unmistakable in the main app
- Tool package (TF‑IDF retrieval + summarize + stats + plotting + log search): [integrated_system/agent/tools.py](integrated_system/agent/tools.py)
- Tool schemas (agent tool definitions): [integrated_system/agent/tool_schemas.py](integrated_system/agent/tool_schemas.py)
- Agent loop implementation: [integrated_system/agent/agent.py](integrated_system/agent/agent.py)
- Integrated “tool-trace” mode in the main pipeline agent: [integrated_system/app/ai_app/agent.py](integrated_system/app/ai_app/agent.py)
- UI toggle + trace visualization: [integrated_system/app/app.py](integrated_system/app/app.py)

### Lab 7 (Reproducibility)
- One-command reproduce script: [reproduce.sh](reproduce.sh) and [scripts/reproduce.sh](scripts/reproduce.sh)
- Root dependency entrypoint: [requirements.txt](requirements.txt)
- Integrated pinned requirements: [integrated_system/config/requirements.txt](integrated_system/config/requirements.txt)

### Lab 8 (Domain adaptation)
- Training scripts + instruction datasets + evaluation JSON: [integrated_system/domain_adaptation/](integrated_system/domain_adaptation/)
- Adapter used for inference (if available locally): [integrated_system/app/lab8_adapted_model/](integrated_system/app/lab8_adapted_model/)

### Lab 9 (Enhancements: monitoring/logging/deployment)
- Monitoring + health/metrics endpoints: [integrated_system/app/api.py](integrated_system/app/api.py) and [integrated_system/app/ai_app/monitoring.py](integrated_system/app/ai_app/monitoring.py)
- Deployment docs + configs: [integrated_system/deployment/](integrated_system/deployment/)

### Project 2 core (KB + retrieval + warehouse + app)
- Knowledge base search: [integrated_system/app/ai_app/knowledge_base.py](integrated_system/app/ai_app/knowledge_base.py)
- Snowflake (live/fallback facts): [integrated_system/app/ai_app/snowflake_service.py](integrated_system/app/ai_app/snowflake_service.py)
- Model wrapper + fallback behavior: [integrated_system/app/ai_app/model_service.py](integrated_system/app/ai_app/model_service.py)

### Added explicit KB ingestion (grade-risk fix)
- KB ingestion script that builds [integrated_system/app/knowledge_base.json](integrated_system/app/knowledge_base.json) from Markdown docs: [src/data/ingest_kb.py](src/data/ingest_kb.py)

## How to run (reproducibility proof)

### One-command
Run `bash reproduce.sh` from the repo root.

### Manual
- Backend: `uvicorn integrated_system.app.api:app --reload --port 8000`
- Frontend: `streamlit run integrated_system/app/app.py`
- Evaluation: `python -m integrated_system.evaluation.evaluate_pipeline`

## Evaluation results (links + summary)

### A) Integrated end-to-end evaluation (retrieval + warehouse grounding + agent reasoning)
- Captured output log: [logs/evaluate_pipeline_output.txt](logs/evaluate_pipeline_output.txt)

Summary from the latest run:
- 3 scenarios executed
- Retrieved documents per scenario: 2–3
- Warehouse facts per scenario: 3
- Reasoning steps per scenario: 5
- Model fallback used: True (expected if a local base model is not provided at runtime)

### B) Lab 6 evaluation evidence
- Lab 6 evaluation report: [docs/evidence/task4_evaluation_report.md](docs/evidence/task4_evaluation_report.md)
- Antigravity IDE analysis report: [docs/evidence/task1_antigravity_report.md](docs/evidence/task1_antigravity_report.md)

### C) Agent chooses tools (multi-step trace proof)
When the Streamlit toggle “Enable Lab 6 tool-agent” is enabled, the backend returns a tool trace showing multi-step tool use.
The tool chain includes:
- retrieve_docs → summarize_text → compute_stats → make_plot_from_counts → search_project_logs

## Percentage contribution
100% (individual submission)

## Tools used
- VS Code
- Git/GitHub
- Python virtual environments
- GitHub Copilot (GPT-5.2) for navigation and drafting

## Reflection
This project strengthened my integration skills across multiple lab deliverables (agent/tooling, reproducibility, domain adaptation, monitoring/deployment) while ensuring the final system is runnable, well-evidenced, and organized for grading. The biggest risks were missing rubric-expected artifacts (diagram image, ingestion script, visible agent tool-use); I addressed these by generating [diagram.png](diagram.png), adding [src/data/ingest_kb.py](src/data/ingest_kb.py), and wiring a tool-trace mode into the main FastAPI + Streamlit workflow.
