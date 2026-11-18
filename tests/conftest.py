"""Shared fixtures for local filesystem ingestion tests."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Callable

import pytest

from query_parser import IngestionQuery

WriteNotebookFunc = Callable[[str, dict[str, Any]], Path]


@pytest.fixture
def sample_query() -> IngestionQuery:
    """Return a query with default local-scan options."""
    return IngestionQuery(
        local_path=Path("/tmp/test_repo").resolve(),
        slug="test_repo",
        id=uuid.uuid4(),
        max_file_size=1_000_000,
        ignore_patterns={"*.pyc", "__pycache__", ".git"},
    )


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Create a representative directory tree containing text files."""
    test_dir = tmp_path / "test_repo"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("Hello World")
    (test_dir / "file2.py").write_text("print('Hello')")

    src_dir = test_dir / "src"
    src_dir.mkdir()
    (src_dir / "subfile1.txt").write_text("Hello from src")
    (src_dir / "subfile2.py").write_text("print('Hello from src')")

    subdir = src_dir / "subdir"
    subdir.mkdir()
    (subdir / "file_subdir.txt").write_text("Hello from subdir")
    (subdir / "file_subdir.py").write_text("print('Hello from subdir')")

    for folder, filename, content in (
        ("dir1", "file_dir1.txt", "Hello from dir1"),
        ("dir2", "file_dir2.txt", "Hello from dir2"),
    ):
        directory = test_dir / folder
        directory.mkdir()
        (directory / filename).write_text(content)

    return test_dir


@pytest.fixture
def write_notebook(tmp_path: Path) -> WriteNotebookFunc:
    """Return a helper that writes notebook data as JSON."""
    def _write_notebook(name: str, content: dict[str, Any]) -> Path:
        notebook_path = tmp_path / name
        notebook_path.write_text(json.dumps(content), encoding="utf-8")
        return notebook_path

    return _write_notebook
