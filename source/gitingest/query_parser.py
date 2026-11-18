"""Resolve local files and directories for ingestion."""

from __future__ import annotations

import uuid
from pathlib import Path

from gitingest.schemas import IngestionQuery

__all__ = ["IngestionQuery", "parse_local_dir_path"]


def parse_local_dir_path(path_str: str) -> IngestionQuery:
    """Resolve a path and create its scan configuration."""
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    slug = path.name or str(path)
    return IngestionQuery(local_path=path, slug=slug, id=uuid.uuid4())
