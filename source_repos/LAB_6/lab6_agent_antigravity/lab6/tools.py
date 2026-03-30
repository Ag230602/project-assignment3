from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RetrievalHit:
    path: str
    score: float
    snippet: str


def _load_corpus(docs_dir: str) -> Tuple[List[str], List[str]]:
    paths = []
    texts = []
    for ext in ("*.txt", "*.md"):
        for p in glob.glob(os.path.join(docs_dir, "**", ext), recursive=True):
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    t = f.read()
                if t.strip():
                    paths.append(p)
                    texts.append(t)
            except Exception:
                # ignore unreadable files
                continue
    return paths, texts


def retrieve_docs(query: str, docs_dir: str = "data/docs", top_k: int = 4) -> Dict[str, Any]:
    """Retrieve relevant local documents (TF‑IDF).

    Args:
        query: User query string.
        docs_dir: Directory containing .md/.txt docs.
        top_k: Number of results to return.

    Returns:
        dict with keys: ok, hits (list), error (optional)
    """
    try:
        paths, texts = _load_corpus(docs_dir)
        if not texts:
            return {"ok": False, "error": f"No documents found in {docs_dir}. Add .md/.txt files."}

        vect = TfidfVectorizer(stop_words="english")
        X = vect.fit_transform(texts)
        q = vect.transform([query])
        sims = cosine_similarity(q, X).flatten()

        idxs = sims.argsort()[::-1][: max(1, top_k)]
        hits: List[Dict[str, Any]] = []
        for i in idxs:
            snippet = texts[i][:400].replace("\n", " ")
            hits.append({"path": paths[i], "score": float(sims[i]), "snippet": snippet})

        return {"ok": True, "hits": hits}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def summarize_text(text: str, max_sentences: int = 5) -> Dict[str, Any]:
    """Simple extractive summarizer (no LLM required).

    Uses sentence splitting + keeps the first N informative sentences.
    """
    try:
        # basic cleanup
        t = re.sub(r"\s+", " ", text).strip()
        if not t:
            return {"ok": False, "error": "Empty text."}

        # naive sentence split
        sentences = re.split(r"(?<=[.!?])\s+", t)
        # keep non-trivial sentences
        keep = [s for s in sentences if len(s) > 40][: max_sentences]
        summary = " ".join(keep) if keep else (t[:400] + ("..." if len(t) > 400 else ""))
        return {"ok": True, "summary": summary}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def compute_stats(text: str) -> Dict[str, Any]:
    """Compute lightweight analytics on text: length, top keywords, counts."""
    try:
        t = re.sub(r"\s+", " ", text).strip()
        if not t:
            return {"ok": False, "error": "Empty text."}

        words = re.findall(r"[A-Za-z][A-Za-z\-']+", t.lower())
        n_words = len(words)
        n_chars = len(t)

        stop = set([
            "the","a","an","and","or","to","of","in","on","for","with","is","are","was","were","be","as","by",
            "it","this","that","from","at","we","you","they","their","our","can","may","will"
        ])
        freq: Dict[str, int] = {}
        for w in words:
            if w in stop or len(w) < 4:
                continue
            freq[w] = freq.get(w, 0) + 1

        top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return {"ok": True, "n_chars": n_chars, "n_words": n_words, "top_keywords": top}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def make_plot_from_counts(items: List[Tuple[str, int]], out_path: str = "lab6/outputs/keyword_plot.png") -> Dict[str, Any]:
    """Create a bar chart from (label, count) pairs and save to disk."""
    try:
        import matplotlib.pyplot as plt

        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        labels = [k for k, _ in items]
        values = [v for _, v in items]

        plt.figure()
        plt.bar(labels, values)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(out_path, dpi=150)
        plt.close()

        return {"ok": True, "path": out_path, "n": len(items)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def search_project_logs(keyword: str, logs_dir: str = "lab6/logs", max_matches: int = 20) -> Dict[str, Any]:
    """Search log files for a keyword and return matching lines."""
    try:
        matches = []
        for p in glob.glob(os.path.join(logs_dir, "**", "*.txt"), recursive=True):
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if keyword.lower() in line.lower():
                            matches.append({"path": p, "line": line.strip()})
                            if len(matches) >= max_matches:
                                break
            except Exception:
                continue
            if len(matches) >= max_matches:
                break
        return {"ok": True, "matches": matches}
    except Exception as e:
        return {"ok": False, "error": str(e)}
