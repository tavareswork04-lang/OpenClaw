"""Async storage helpers for saving scraped data."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from io import StringIO
from pathlib import Path

import aiofiles

from openclaw.utils import get_logger

logger = get_logger()

OUTPUT_DIR = Path("output")


class StorageManager:
    """Save structured data asynchronously to disk."""

    @staticmethod
    async def save(data: list[dict], fmt: str = "json") -> Path:
        """Persist *data* to a timestamped file in the output directory.

        Parameters
        ----------
        data:
            List of record dictionaries.
        fmt:
            ``"json"`` (default) or ``"csv"``.

        Returns
        -------
        Path
            Absolute path of the written file.
        """
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"openclaw_{timestamp}.{fmt}"

        if fmt == "json":
            content = json.dumps(data, ensure_ascii=False, indent=2)
            async with aiofiles.open(filename, "w", encoding="utf-8") as fh:
                await fh.write(content)

        elif fmt == "csv":
            if not data:
                filename.touch()
            else:
                buf = StringIO()
                writer = csv.DictWriter(buf, fieldnames=list(data[0].keys()))
                writer.writeheader()
                writer.writerows(data)
                async with aiofiles.open(filename, "w", encoding="utf-8", newline="") as fh:
                    await fh.write(buf.getvalue())
        else:
            raise ValueError(f"Unsupported format: {fmt!r}. Choose 'json' or 'csv'.")

        logger.info("Data saved to %s (%d records)", filename, len(data))
        return filename
