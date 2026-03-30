# System Architecture

```mermaid
flowchart LR
    A[Data Sources] --> B[Knowledge Base]
    B --> C[Retrieval Pipeline]
    C --> D[Domain-Adapted Model]
    C --> E[Snowflake Warehouse]
    D --> F[AI Agent Reasoning Layer]
    E --> F
    F --> G[FastAPI / Streamlit Application]
    G --> H[Monitoring, Logging, Evaluation]
```

## Component placement in this folder
- `integrated_system/retrieval/` -> retrieval pipeline
- `integrated_system/domain_adaptation/` -> LoRA / PEFT work
- `integrated_system/agent/` -> agent logic and tools
- `integrated_system/warehouse/` -> Snowflake code
- `integrated_system/app/` -> API + Streamlit UI
- `integrated_system/evaluation/` -> benchmarks and example outputs
- `integrated_system/deployment/` -> Render/Railway deployment files
