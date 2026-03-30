from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None

from collections import Counter


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
        # If called from the integrated repo root, prefer the Lab 6 docs folder when it exists.
        if docs_dir == "data/docs":
            candidate = os.path.join("source_repos", "LAB_6", "lab6_agent_antigravity", "data", "docs")
            if os.path.isdir(candidate):
                docs_dir = candidate
        paths, texts = _load_corpus(docs_dir)
        if not texts:
            return {"ok": False, "error": f"No documents found in {docs_dir}. Add .md/.txt files."}

        sims = None
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
            from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

            vect = TfidfVectorizer(stop_words="english")
            X = vect.fit_transform(texts)
            q = vect.transform([query])
            sims = cosine_similarity(q, X).flatten()
            idxs = sims.argsort()[::-1][: max(1, top_k)]
        except Exception:
            # Fallback: lexical overlap scoring (keeps the tool usable without sklearn).
            q_tokens = [tok for tok in re.findall(r"[A-Za-z0-9]+", query.lower()) if len(tok) > 2]
            q_counts = Counter(q_tokens)

            scored = []
            for i, text in enumerate(texts):
                t_tokens = [tok for tok in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(tok) > 2]
                t_counts = Counter(t_tokens)
                score = sum(q_counts[tok] * t_counts.get(tok, 0) for tok in q_counts)
                scored.append((i, float(score)))
            scored.sort(key=lambda pair: pair[1], reverse=True)
            idxs = [i for i, _ in scored[: max(1, top_k)]]

        hits: List[Dict[str, Any]] = []
        for i in idxs:
            snippet = texts[i][:400].replace("\n", " ")
            score = float(sims[i]) if sims is not None else 0.0
            hits.append({"path": paths[i], "score": score, "snippet": snippet})

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


def make_plot_from_counts(items: List[Tuple[str, int]], out_path: str = "integrated_system/logs/lab6_keyword_plot.png") -> Dict[str, Any]:
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


def search_project_logs(keyword: str, logs_dir: str = "integrated_system/logs", max_matches: int = 20) -> Dict[str, Any]:
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
