"""Public local filesystem ingestion API."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from config import MAX_FILE_SIZE
from ingestion import ingest_query
from query_parser import parse_local_dir_path
from utils.ignore_patterns import load_ignore_patterns
from utils.pattern_utils import process_patterns


async def ingest_async(
    source: str,
    *,
    max_file_size: int = MAX_FILE_SIZE,
    include_patterns: str | set[str] | None = None,
    exclude_patterns: str | set[str] | None = None,
    include_gitignored: bool = False,
    output: str | None = None,
) -> tuple[str, str, str]:
    """Scan a local file or directory and optionally write its digest."""
    query = parse_local_dir_path(source)
    query.max_file_size = max_file_size
    query.ignore_patterns, query.include_patterns = process_patterns(
        exclude_patterns=exclude_patterns, include_patterns=include_patterns,
    )
    if not include_gitignored and query.local_path.is_dir():
        for filename in (".gitignore", ".gitingestignore", ".ignore", "*.ignore"):
            query.ignore_patterns.update(load_ignore_patterns(query.local_path, filename=filename))
    result = ingest_query(query)
    if output is not None:
        data = f"{result[1]}\n{result[2]}"
        if output == "-":
            sys.stdout.write(data)
            sys.stdout.flush()
        else:
            Path(output).write_text(data, encoding="utf-8")
    return result


def ingest(source: str, **kwargs: object) -> tuple[str, str, str]:
    """Synchronous wrapper around :func:`ingest_async`."""
    return asyncio.run(ingest_async(source, **kwargs))
