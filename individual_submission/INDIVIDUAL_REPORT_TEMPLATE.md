# Individual Contribution Report Template

## Name
Adrija Ghosh

## Project
Project 3 Integrated GenAI System

## Personal Contribution Summary
This is an individual submission. I independently integrated the outputs of Labs 6–9 into a single Project 3 GenAI system, wired them into the provided integrated_system scaffold, and verified that the end-to-end pipeline (retrieval, domain-adapted model, agent, Snowflake wrapper, API, UI, evaluation, and deployment docs) runs successfully. I was responsible for copying, organizing, and connecting all Python modules, configuration files, logs, and artifacts needed for the final submission, as well as documenting reproducibility and my own contributions.

## Technical Work Completed
- **Agent integration work (Lab 6)**: Integrated the Lab 6 agent and tools into the final project under integrated_system/agent/, including agent.py, tools.py, tool_schemas.py, and the Streamlit agent interface; moved agent logs into integrated_system/logs/ and added evaluation reports under docs/evidence/.
- **Reproducibility work (Lab 7)**: Merged dependencies into a single integrated_system/config/requirements.txt, copied the reproduce.sh script, pulled over Lab 7 logs, and filled docs/reproducibility_notes.md with Python version, environment variables, and commands to run smoke tests, backend, frontend, and evaluation.
- **Domain adaptation / LoRA work (Lab 8)**: Integrated instruction_dataset*.json, lab8_individual_lora*.py, lab8_adapted_model/, and evaluation_results*.json into integrated_system/domain_adaptation/, ensuring the adapted model and training scripts are available for inspection and reuse in the final pipeline.
- **UI / deployment / evaluation work (Lab 8/9)**: Copied the FastAPI backend (api.py), Streamlit UI (app.py), knowledge_base.json, and the full ai_app package into integrated_system/app/, along with lab8_adapted_model/ for inference; copied render.yaml, DEPLOYMENT.md, and RAILWAY_DEPLOYMENT.md into integrated_system/deployment/ to document cloud deployment.
- **Integrated retrieval, warehouse, and evaluation wrappers (Project 3 glue code)**: Implemented thin wrapper modules retrieval_service.py, warehouse_service.py, and evaluate_pipeline.py under integrated_system/retrieval/, integrated_system/warehouse/, and integrated_system/evaluation/ so that other components can call a stable retrieval API, SnowflakeService, and evaluation entrypoint without importing directly from lab folders.
- **End-to-end verification**: Turned integrated_system into a Python package with __init__.py files and ran python -m integrated_system.evaluation.evaluate_pipeline to confirm that the DisasterForecastAgent, knowledge base retrieval, Snowflake fallback, and evaluation loop execute end-to-end without errors.

## Percentage Contribution
My contribution to the final project: 100 %

## GitHub Evidence
- LAB_6 repository: LAB_6/lab6_agent_antigravity/lab6/ (agent.py, tools.py, tool_schemas.py, streamlit_app.py, logs, evaluation reports) integrated into integrated_system/agent/, integrated_system/logs/, and docs/evidence/.
- LAB_7 repository: LAB_7/ (requirements.txt, logs/, cs5542_reproducibility_template/reproduce.sh, reproducibility template) merged into integrated_system/config/requirements.txt, integrated_system/logs/, scripts/reproduce.sh, and docs/reproducibility_notes.md.
- Lab 8 repository: lab_8/Lab8_Individual_Submission_Adrija/ (instruction_dataset*.json, lab8_individual_lora*.py, lab8_adapted_model/, evaluation_results*.json) copied into integrated_system/domain_adaptation/ and integrated_system/app/.
- Lab 9 repository: lab_9/Lab8_Individual_Submission_Adrija/ (ai_app/, api.py, app.py, knowledge_base.json, render.yaml, deployment docs) copied into integrated_system/app/ and integrated_system/deployment/.
- Project 3 integrated folder: this submission’s integrated_system/, docs/, scripts/, and individual_submission/ directories reflect my integration and documentation work.

## Tools Used
- VS Code as the primary development environment
- Git and GitHub for version control and copying lab repositories into the integrated folder
- Python virtual environments for dependency isolation
- Generative AI coding assistants (including GitHub Copilot using GPT-5.1 and related tools) for code navigation, boilerplate generation, and documentation drafting

## Reflection
Through this project I learned how to take several partially independent lab deliverables and turn them into a single, coherent GenAI system with a clear architecture and reproducible setup. The main challenges were managing multiple repositories and overlapping files, merging requirements without breaking dependencies, and ensuring that the final integrated_system layout matched the course scaffold while still running end-to-end. I addressed these challenges by carefully following MERGE_MAP.md, adding small wrapper modules instead of rewriting existing code, and verifying the pipeline with evaluation scripts and smoke tests. Overall, this work strengthened my skills in system integration, environment management, and documenting complex GenAI applications as an individual contributor.
