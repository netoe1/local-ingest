"""Small standard-library logging setup for offline use."""

from __future__ import annotations

import logging
import os
import sys


def configure_logging() -> None:
    """Configure application logs on stderr."""
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        stream=sys.stderr,
        force=True,
    )


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a standard library logger."""
    return logging.getLogger(name)


configure_logging()
