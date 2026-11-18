"""Tests for resolving local scan paths."""

from pathlib import Path

import pytest

from query_parser import parse_local_dir_path


def test_parse_local_directory(tmp_path: Path) -> None:
    query = parse_local_dir_path(str(tmp_path))

    assert query.local_path == tmp_path.resolve()
    assert query.slug == tmp_path.name


def test_parse_local_file(tmp_path: Path) -> None:
    file_path = tmp_path / "notes.txt"
    file_path.write_text("hello", encoding="utf-8")

    query = parse_local_dir_path(str(file_path))

    assert query.local_path == file_path.resolve()


def test_parse_missing_path_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        parse_local_dir_path(str(tmp_path / "missing"))


def test_each_parse_gets_a_unique_id(tmp_path: Path) -> None:
    first = parse_local_dir_path(str(tmp_path))
    second = parse_local_dir_path(str(tmp_path))

    assert first.id != second.id
