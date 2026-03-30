# Project 3 — Integrated System Submission Guide

This file is a **single place** that explains what’s in this folder, shows the **end-to-end pipeline**, links to **all key code + evidence + evaluation**, includes **contribution + individual submission artifacts**, and ends with **exact steps to push to GitHub**.

---

## 0) One-line core idea (grading)

**One complete AI system integrating:**
Data → Retrieval (RAG) → Domain-Adapted Model → Agent (multi-step tools) → Snowflake → App → Evaluation + Logs → Reproducibility.

---

## 1) Pipeline diagram (required)

![Project 3 architecture diagram](diagram.png)

- Diagram source generator: `scripts/generate_diagram_png.py`
- Mermaid architecture notes (optional): `docs/SYSTEM_ARCHITECTURE.md`

---

## 2) What each top-level item is for (folder tour)

### Key top-level entrypoints
- `README.md` — quick overview + diagram embed
- `RUN.md` — exact run commands (backend, Streamlit, evaluation, rebuild KB, regenerate diagram)
- `reproduce.sh` — one-command wrapper for reproducibility
- `scripts/reproduce.sh` — installs deps + runs integrated evaluation
- `requirements.txt` — grading-friendly root requirements entrypoint (includes `integrated_system/config/requirements.txt`)

### Rubric-friendly expected structure
Some rubrics expect `src/`, `evaluation/`, `logs/`, and `configs/` at the root.
This repo includes them as thin wrappers around the real implementation:
- `src/` — rubric-friendly imports/wrappers; actual system lives in `integrated_system/`
- `evaluation/` — wrapper entrypoint (`evaluation/evaluate_pipeline.py`) calling the integrated evaluation
- `logs/` — root-level logs (e.g., `logs/evaluate_pipeline_output.txt`)
- `configs/` — environment template + requirements mirror

### The real working system
- `integrated_system/` — the full integrated pipeline (agent, retrieval, model, Snowflake service, app, evaluation, logs)

### Evidence + reports
- `docs/evidence/` — Lab 6 evidence reports
- `reports/` — project report template + contribution tables
- `individual_submission/` — individual report template + filled individual report

### Provenance (where things came from)
- `source_repos/` — upstream lab repos included for reference
- `MERGE_MAP.md` — mapping of what was merged from which lab
- `source_links.txt` — any reference links

---

## 3) Where each pipeline layer lives (with links)

### Data Sources → Knowledge Base
- Knowledge base JSON used by the app: `integrated_system/app/knowledge_base.json`
- KB ingestion script (build from Markdown docs): `src/data/ingest_kb.py`
  - Example input docs include: `source_repos/LAB_6/lab6_agent_antigravity/data/docs/`

### Retrieval (RAG)
- Lightweight lexical similarity retrieval used by the main app: `integrated_system/app/ai_app/knowledge_base.py`
- Wrapper service for stable retrieval API: `integrated_system/retrieval/retrieval_service.py`

### Domain-Adapted Model (Lab 8)
- Model loading + PEFT adapter logic: `integrated_system/app/ai_app/model_service.py`
- LoRA / domain adaptation artifacts + scripts: `integrated_system/domain_adaptation/`
- Inference adapter path in app package: `integrated_system/app/lab8_adapted_model/`

### AI Agent (multi-step reasoning + tool use) — Lab 6 integrated
There are **two** relevant agent layers:

1) **Main integrated agent** (used by FastAPI `/generate`):
- `integrated_system/app/ai_app/agent.py`
  - Retrieves KB context
  - Pulls Snowflake / fallback facts
  - Builds a grounded prompt
  - Generates response via adapted model (or safe fallback)
  - **Optional Lab 6 multi-tool trace** when `use_lab6_agent=true`

2) **Lab 6 tool-agent package** (tools + tool schemas + standalone Streamlit):
- `integrated_system/agent/agent.py`
- `integrated_system/agent/tools.py`
- `integrated_system/agent/tool_schemas.py`
- `integrated_system/agent/streamlit_app.py`

### Snowflake (data queries)
- Snowflake live query + fallback facts: `integrated_system/app/ai_app/snowflake_service.py`
- Thin warehouse wrapper module: `integrated_system/warehouse/warehouse_service.py`

### App layer
- FastAPI backend: `integrated_system/app/api.py`
- Streamlit UI: `integrated_system/app/app.py`

### Evaluation + Logs
- Integrated evaluation entrypoint: `integrated_system/evaluation/evaluate_pipeline.py`
- Root wrapper evaluation entrypoint: `evaluation/evaluate_pipeline.py`
- Logs:
  - Integrated logs folder: `integrated_system/logs/`
  - Root logs folder: `logs/`

---

## 4) Reproducibility (Lab 7)

### One-command run

```bash
bash reproduce.sh
```

This calls `scripts/reproduce.sh` which:
- installs dependencies via `requirements.txt`
- runs integrated evaluation and writes logs under `logs/`

### Manual run commands

```bash
# Backend
uvicorn integrated_system.app.api:app --reload --port 8000

# Frontend
streamlit run integrated_system/app/app.py

# Evaluation
python -m integrated_system.evaluation.evaluate_pipeline
```

Reproducibility notes: `docs/reproducibility_notes.md`

---

## 5) Evaluation results (what to show graders)

### A) Integrated system evaluation (end-to-end)
- Output log (captured): `logs/evaluate_pipeline_output.txt`

Summary (latest run):
- Scenario count: 3
- Retrieved documents: 2–3 per scenario
- Warehouse facts: 3 per scenario
- Reasoning steps: 5 per scenario
- Model fallback: True (expected if no local base model is provided)

### B) Lab 6 evaluation evidence (agent-enabled RAG)
- `docs/evidence/task4_evaluation_report.md`
- `docs/evidence/task1_antigravity_report.md`

### C) Lab 6 multi-tool trace proof (agent chooses tools)
The integrated app can return a tool trace when the UI toggle is enabled.

Example trace (tools executed):
- `retrieve_docs`
- `summarize_text`
- `compute_stats`
- `make_plot_from_counts`
- `search_project_logs`

A plot artifact may be produced at:
- `integrated_system/logs/lab6_keyword_plot.png`

---

## 6) Contribution + individual submission artifacts

### Contribution table
- Individual submission (100%): `reports/CONTRIBUTION_TABLE.csv`

### Individual report
- Filled individual report: `individual_submission/INDIVIDUAL_REPORT.md`
- Template (if needed): `individual_submission/INDIVIDUAL_REPORT_TEMPLATE.md`

---

## 7) What you should mention in your 5–8 page report (quick mapping)

Use `reports/PROJECT3_REPORT_TEMPLATE.md`, and make sure the following are **explicit**:
- End-to-end pipeline (include `diagram.png`)
- Agent with tool trace (Lab 6)
- Reproducibility (Lab 7): exact commands
- Domain adaptation artifacts (Lab 8)
- Enhancements / monitoring / deployment docs (Lab 9)
- Evaluation proof (logs + evidence reports)

---

## 8) Push this entire folder to GitHub (macOS, exact steps)

### Step 1 — Create a new GitHub repo
On GitHub.com:
1. Click **New repository**
2. Name it (example): `project3-integrated-system`
3. Keep it **Public or Private** based on class rules
4. Do **NOT** initialize with a README (this folder already has one)

### Step 2 — Initialize git locally and commit
From this folder root:

```bash
cd /path/to/Project3_Integrated_Folder

git init
git add -A
git commit -m "Project 3 integrated submission"
```

### Step 3 — Add remote and push
Replace the URL with your repo URL:

```bash
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
git push -u origin main
```

### If GitHub rejects the push
Common reasons:
- Missing authentication (use GitHub Desktop, or create a Personal Access Token)
- Large files (GitHub blocks files >100MB)

This repo was scanned for >90MB files and none were detected, but if GitHub still complains, run:

```bash
find . -type f -size +90M -print
```

If you do have large model weight files, use **Git LFS**:

```bash
git lfs install
git lfs track "*.safetensors"
git add .gitattributes
git add -A
git commit -m "Track large model files with Git LFS"
git push
```

---

## 9) Quick “grader demo” checklist

1. Show `diagram.png`
2. Run `bash reproduce.sh`
3. Start API + Streamlit and run one query
4. Enable **Lab 6 tool-agent** toggle and show the tool trace
5. Show evaluation output log + Lab 6 evidence reports
6. Show contribution + individual report
