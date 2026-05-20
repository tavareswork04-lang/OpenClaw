"""Utility helpers for OpenClaw."""

from __future__ import annotations

import logging
import os
from functools import lru_cache


@lru_cache(maxsize=None)
def get_logger(name: str = "openclaw") -> logging.Logger:
    """Return (and cache) a named logger with sensible defaults."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger(name)


def get_env(key: str, default: str | None = None) -> str | None:
    """Read *key* from environment variables, falling back to *default*."""
    return os.environ.get(key, default)
