
# CS 5542 – Lab 6: Agent-enabled RAG System

## Project Overview
This project extends the previous Retrieval-Augmented Generation (RAG) pipeline by integrating an AI agent layer capable of reasoning over user queries, selecting tools, retrieving evidence, and generating grounded responses.

The system demonstrates how an AI agent can interact with tools to perform retrieval and produce responses supported by evidence citations.

---

## System Architecture

The system consists of four major components:

1. **Agent Layer**
   - Interprets user queries
   - Decides which tools to use
   - Executes reasoning steps

2. **Tool Layer**
   - Retrieval of evidence from dataset
   - Execution of RAG queries
   - Logging metrics

3. **Retrieval System**
   - Hybrid retrieval using TF-IDF, BM25, and dense embeddings
   - Evidence selection from dataset metadata

4. **User Interface**
   - Streamlit chat interface
   - Displays responses and evidence citations

---

## Repository Structure

```
lab6/
│
├── agent.py                 # AI agent implementation
├── tools.py                 # Retrieval and RAG tool functions
├── tool_schemas.py          # Tool definitions for the agent
├── streamlit_app.py         # Streamlit chat interface
│
├── logs/
│   ├── agent_query_metrics.csv
│   └── agent_execution_log.txt
│
├── screenshots/             # Antigravity IDE screenshots
│
task1_antigravity_report.md  # Antigravity IDE analysis report
task4_evaluation_report.md   # Evaluation report
CONTRIBUTION.md              # Individual contribution document
README.md                    # Project documentation
```

---

## How to Run the Project

### 1. Install Dependencies

Run:

```
pip install numpy pandas scikit-learn rank-bm25 sentence-transformers streamlit openai
```

### 2. Run the Streamlit Application

```
streamlit run lab6/streamlit_app.py
```

Then open:

```
http://localhost:8501
```

---

## Example Queries

Simple Query:
```
What documents are available in the dataset?
```

Medium Query:
```
Summarize the repository structure.
```

Complex Query:
```
Explain how retrieval and grounding work together in this system.
```

---

## Evaluation

The agent was evaluated using three scenarios:

| Scenario | Query Type | Tool Used | Latency |
|--------|--------|--------|--------|
| Simple | Dataset query | tool_run_rag_query | ~20 ms |
| Medium | Repository summary | tool_run_rag_query | ~20 ms |
| Complex | System explanation | tool_run_rag_query | ~22 ms |

Detailed results are provided in:

```
task4_evaluation_report.md
```

---

## Logs

System execution logs are automatically generated in:

```
lab6/logs/
```

Files:

```
agent_query_metrics.csv
agent_execution_log.txt
```

These logs contain latency metrics, retrieval information, and agent tool execution details.

---

## Demo Video

Demo video (3–5 minutes):https://youtu.be/1SV0GcmFMgQ


The video demonstrates:

• Running the Streamlit application  
• Asking queries  
• Evidence-based responses  
• Log generation  

---

## Key Features

• Agent-based reasoning over user queries  
• Tool calling architecture  
• Hybrid document retrieval  
• Grounded responses with citations  
• Streamlit interactive chat interface  
• Automatic evaluation logging  

---

## Conclusion

This implementation demonstrates a functional agent-enabled RAG system integrating retrieval, reasoning, tool execution, and interactive user interface.

The system represents a significant step toward the final project architecture for CS 5542.
