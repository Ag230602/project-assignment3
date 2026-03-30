import json
import math
import re
from collections import Counter

from .config import KNOWLEDGE_BASE_PATH


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class KnowledgeBase:
    def __init__(self, path=KNOWLEDGE_BASE_PATH):
        self.path = path
        self.documents = self._load_documents()

    def _load_documents(self) -> list[dict]:
        with open(self.path, encoding="utf-8") as file:
            docs = json.load(file)

        prepared = []
        for doc in docs:
            content = doc.get("content", "")
            tokens = _tokenize(" ".join([doc.get("title", ""), content]))
            prepared.append(
                {
                    **doc,
                    "tokens": tokens,
                    "term_counts": Counter(tokens),
                    "norm": math.sqrt(sum(count * count for count in Counter(tokens).values()))
                    or 1.0,
                }
            )
        return prepared

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        query_counts = Counter(_tokenize(query))
        query_norm = math.sqrt(sum(count * count for count in query_counts.values())) or 1.0
        scored = []

        for doc in self.documents:
            numerator = sum(
                query_counts[token] * doc["term_counts"].get(token, 0) for token in query_counts
            )
            score = numerator / (query_norm * doc["norm"])
            if score > 0:
                scored.append({**doc, "score": round(score, 4)})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return [
            {
                "title": doc["title"],
                "content": doc["content"],
                "source_type": doc.get("source_type", "knowledge_base"),
                "score": doc["score"],
                "metadata": doc.get("metadata", {}),
            }
            for doc in scored[:top_k]
        ]
