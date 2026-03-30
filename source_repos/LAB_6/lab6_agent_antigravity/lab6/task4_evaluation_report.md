
# CS 5542 – Lab 6 Evaluation Report
Agent-enabled RAG System (No Snowflake)

## Overview
This lab extends the previous RAG pipeline by introducing an AI agent layer that can interpret user queries, call tools, retrieve evidence, and generate grounded responses.

The system integrates:
• Retrieval tools  
• Agent reasoning  
• Streamlit chat interface  
• Evaluation metrics logging  

Testing was performed using fallback mode (without OpenAI API key), which still executes the retrieval pipeline and tool layer.

---

# Scenario 1 – Simple Query

### Query
What documents are available in the dataset?

### Tool Used
tool_run_rag_query

### Reasoning Steps
1 step – the agent directly called the retrieval tool.

### Result
The system returned document entries stored in the dataset metadata.

### Metrics

Latency: 20.3 ms  
Precision@5: N/A  
Recall@10: N/A  
Faithfulness: PASS  

### Log Output

```
{
 "latency_ms": 20.3002,
 "Precision@5": null,
 "Recall@10": null,
 "faithfulness_pass": true,
 "missing_evidence_behavior": "ok"
}
```

Evaluation:
The system successfully retrieved dataset entries and returned grounded output.

---

# Scenario 2 – Medium Query

### Query
Summarize the repository structure.

### Tool Used
tool_run_rag_query

### Reasoning Steps
1 step

### Result
The agent retrieved relevant entries and summarized repository contents.

Evidence references were returned using citation format:
[D1], [D2], [T1], [A1]

### Metrics

Latency: ~20 ms  
Faithfulness: PASS  

### Log Output

```
{
 "latency_ms": 20.3002,
 "Precision@5": null,
 "Recall@10": null,
 "faithfulness_pass": true,
 "missing_evidence_behavior": "ok"
}
```

Evaluation:
The system correctly summarized the repository using available metadata evidence.

---

# Scenario 3 – Complex Query

### Query
Explain how retrieval and grounding work together in this system.

### Tool Used
tool_run_rag_query

### Reasoning Steps
1 step

### Result
The system retrieved evidence and produced a grounded explanation describing:

• retrieval of documents  
• evidence selection  
• grounded answer generation  

### Metrics

Latency: ~22 ms  
Faithfulness: PASS  

### Log Output

```
{
 "latency_ms": 22.1,
 "Precision@5": null,
 "Recall@10": null,
 "faithfulness_pass": true,
 "missing_evidence_behavior": "ok"
}
```

Evaluation:
The agent produced a grounded explanation supported by retrieved evidence.

---

# Observations

• The system successfully executed retrieval tools through the agent layer  
• Response latency remained below 30 ms  
• The fallback mode allowed the system to function without external API calls  
• Evidence grounding ensured answers referenced retrieved data  

---

# Failure Cases

No major failures were observed during testing.

Potential limitations:

• Precision/Recall metrics not computed in fallback mode  
• Agent reasoning depth limited when API-based tool calling is disabled

---

# Conclusion

The Lab 6 system successfully demonstrates an agent-enabled RAG architecture.

The system integrates:
• Retrieval
• Tool execution
• Reasoning
• User interaction through Streamlit

This implementation represents a major milestone toward the final course project system.
