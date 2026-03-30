from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def _iter_markdown_files(input_dirs: list[Path]) -> Iterable[Path]:
    for input_dir in input_dirs:
        if not input_dir.exists():
            continue
        for path in input_dir.rglob("*.md"):
            if path.is_file():
                yield path


def _extract_title(text: str, fallback: str) -> str:
    match = TOKEN_PATTERN.search(text)
    if match:
        return match.group(1).strip()[:120]
    return fallback


def _chunk_text(text: str, chunk_chars: int, overlap: int) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []

    if len(cleaned) <= chunk_chars:
        return [cleaned]

    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + chunk_chars)
        chunks.append(cleaned[start:end])
        if end >= len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks


def build_knowledge_base(
    input_dirs: list[Path],
    source_type: str,
    chunk_chars: int,
    overlap: int,
) -> list[dict]:
    docs: list[dict] = []

    for path in sorted(_iter_markdown_files(input_dirs)):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if not raw.strip():
            continue

        title = _extract_title(raw, fallback=path.stem)
        chunks = _chunk_text(raw, chunk_chars=chunk_chars, overlap=overlap)
        for chunk_index, chunk in enumerate(chunks, start=1):
            docs.append(
                {
                    "title": title if len(chunks) == 1 else f"{title} (part {chunk_index})",
                    "content": chunk,
                    "source_type": source_type,
                    "metadata": {
                        "path": str(path.as_posix()),
                        "chunk_index": chunk_index,
                        "chunks": len(chunks),
                    },
                }
            )

    return docs


def main() -> None:
    parser = argparse.ArgumentParser(description="Build knowledge_base.json from markdown docs.")
    parser.add_argument(
        "--input-dir",
        action="append",
        dest="input_dirs",
        default=[],
        help="Input directory containing .md files (repeatable).",
    )
    parser.add_argument(
        "--output-json",
        default="integrated_system/app/knowledge_base.json",
        help="Output JSON path.",
    )
    parser.add_argument(
        "--source-type",
        default="project_docs",
        help="Value for source_type field in KB documents.",
    )
    parser.add_argument("--chunk-chars", type=int, default=1200)
    parser.add_argument("--overlap", type=int, default=120)

    args = parser.parse_args()

    if not args.input_dirs:
        args.input_dirs = [
            "docs",
            "source_repos/LAB_6/lab6_agent_antigravity/data/docs",
        ]

    input_dirs = [Path(p) for p in args.input_dirs]
    output_path = Path(args.output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    docs = build_knowledge_base(
        input_dirs=input_dirs,
        source_type=args.source_type,
        chunk_chars=args.chunk_chars,
        overlap=args.overlap,
    )

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(docs, handle, indent=2, ensure_ascii=False)

    print(f"Wrote {len(docs)} documents to {output_path}")


if __name__ == "__main__":
    # Allow running as a script from repo root.
    os.chdir(Path(__file__).resolve().parents[2])
    main()
