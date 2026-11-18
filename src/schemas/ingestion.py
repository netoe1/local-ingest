"""Configuration for scanning a local filesystem path."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID

from config import MAX_FILE_SIZE


@dataclass
class IngestionQuery:
    """Options and resolved paths for one local scan."""

    local_path: Path
    slug: str
    id: UUID
    subpath: str = "/"
    max_file_size: int = MAX_FILE_SIZE
    ignore_patterns: set[str] = field(default_factory=set)
    include_patterns: set[str] | None = None
