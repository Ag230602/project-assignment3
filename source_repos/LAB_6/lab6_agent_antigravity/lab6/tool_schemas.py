tool_schemas = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_docs",
            "description": "Search local project documents (data/docs) using TF-IDF and return top matches with snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "docs_dir": {"type": "string", "default": "data/docs"},
                    "top_k": {"type": "integer", "default": 4}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_text",
            "description": "Create a short extractive summary of the provided text (no LLM required).",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "max_sentences": {"type": "integer", "default": 5}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compute_stats",
            "description": "Compute simple analytics on text: length and top keywords.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_plot_from_counts",
            "description": "Generate a bar chart from keyword counts and save it to an image file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": [{"type": "string"}, {"type": "integer"}],
                            "minItems": 2,
                            "maxItems": 2
                        }
                    },
                    "out_path": {"type": "string", "default": "lab6/outputs/keyword_plot.png"}
                },
                "required": ["items"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_project_logs",
            "description": "Search lab6/logs for a keyword and return matching lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "logs_dir": {"type": "string", "default": "lab6/logs"},
                    "max_matches": {"type": "integer", "default": 20}
                },
                "required": ["keyword"]
            }
        }
    }
]
