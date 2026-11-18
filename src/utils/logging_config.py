"""Small standard-library logging setup for offline use."""

from __future__ import annotations

import json
import logging
import os
import sys


_RESET = "\033[0m"
_LEVEL_COLORS = {
    logging.DEBUG: "\033[37m",
    logging.INFO: "\033[32m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[1;31m",
}


class _ColorFormatter(logging.Formatter):
    """Format logs with terminal colors and optional structured fields."""

    def __init__(self, *, use_color: bool) -> None:
        super().__init__()
        self.use_color = use_color
        self._standard_fields = set(logging.makeLogRecord({}).__dict__)

    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        level = f"{record.levelname:<8}"
        logger_name = f"{record.name}:{record.funcName}:{record.lineno}"
        message = record.getMessage()

        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key not in self._standard_fields and not key.startswith("_")
        }
        if extra:
            message = f"{message} | {json.dumps(extra, ensure_ascii=False, default=str)}"

        if self.use_color:
            timestamp = f"\033[2m{timestamp}{_RESET}"
            color = _LEVEL_COLORS.get(record.levelno, "")
            level = f"{color}{level}{_RESET}"
            logger_name = f"\033[36m{logger_name}{_RESET}"

        return f"{timestamp} | {level} | {logger_name} | {message}"


def configure_logging() -> None:
    """Configure application logs on stderr."""
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    color_mode = os.getenv("LOG_COLOR", "auto").lower()
    use_color = color_mode == "always" or (color_mode != "never" and sys.stderr.isatty())
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_ColorFormatter(use_color=use_color))
    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a standard library logger."""
    return logging.getLogger(name)


configure_logging()
