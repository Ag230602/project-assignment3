# Merge Map

Use this file to track what you copy from each repository.

## Source repos

1. LAB_6/lab6_agent_antigravity
2. LAB_7
3. lab_8/Lab8_Individual_Submission_Adrija
4. lab_9/Lab8_Individual_Submission_Adrija

## Recommended merge

### From Lab 6
Copy into `integrated_system/agent/`:
- `agent.py` (copied)
- `tools.py` (copied)
- `tool_schemas.py` (copied)
- `streamlit_app.py` (copied)
- `logs/agent_query_metrics.csv` (copied to `integrated_system/logs/`)
- `logs/agent_execution_log.txt` (copied to `integrated_system/logs/`)
- `task1_antigravity_report.md`, `task4_evaluation_report.md` (copied to `docs/evidence/`)

### From Lab 7
Copy into:
- `integrated_system/config/requirements.txt` (merged requirements from Lab 7 + app)
- `scripts/reproduce.sh` (copied)
- `docs/reproducibility_notes.md` (filled with environment and commands)
- `integrated_system/logs/` (experiment logs copied)
- any smoke tests / environment validation scripts

### From Lab 8
Copy into `integrated_system/domain_adaptation/`:
- `instruction_dataset*.json` (copied)
- `lab8_individual_lora*.py` (copied)
- `lab8_adapted_model/` (copied)
- model evaluation JSON files (copied)

Also copy app/backend pieces into:
- `integrated_system/app/api.py`
- `integrated_system/app/app.py`
- `integrated_system/app/ai_app/` (from Lab 9 latest version)

### From Lab 9
Copy deployment and enhanced app pieces into:
- `integrated_system/deployment/render.yaml`
- `integrated_system/deployment/DEPLOYMENT.md`
- `integrated_system/deployment/RAILWAY_DEPLOYMENT.md`
- enhanced monitoring / logging / evaluation code

### From Project 2
Copy into:
- `integrated_system/retrieval/`
- `integrated_system/warehouse/`
- `integrated_system/app/`
- `integrated_system/evaluation/`

## File conflict checklist

- [ ] `README.md` consolidated
- [ ] duplicate `app.py` resolved
- [ ] duplicate `api.py` resolved
- [ ] requirements merged into one file
- [ ] duplicate dataset / knowledge base files checked
- [ ] logs moved to a single `logs/` folder
- [ ] deployment docs updated for final repo
- [ ] environment variables standardized
