"""Main orchestrator for OpenClaw scraping tasks."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from openclaw.browser import BrowserEngine
from openclaw.scraper import Scraper
from openclaw.storage import StorageManager
from openclaw.utils import get_logger

console = Console()
logger = get_logger()


class OpenClawAgent:
    """High-level agent that orchestrates scraping tasks.

    Parameters
    ----------
    headless:
        Run the browser in headless mode (default: True).
    max_retries:
        Number of retry attempts on page fetch failure (default: 3).
    delay:
        Base delay in seconds between page requests (default: 1.0).
    """

    def __init__(
        self,
        headless: bool = True,
        max_retries: int = 3,
        delay: float = 1.0,
    ) -> None:
        self.headless = headless
        self.max_retries = max_retries
        self.delay = delay

    async def run(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute a scraping task.

        Parameters
        ----------
        task:
            Dictionary with keys:
            - ``url`` (str): Starting URL.
            - ``selectors`` (dict): CSS selectors mapping field names to CSS rules.
            - ``paginate`` (bool): Follow pagination links (default: False).
            - ``max_pages`` (int): Max pages to scrape when paginating (default: 10).
            - ``output_format`` (str): ``"json"`` or ``"csv"`` (default: ``"json"``).

        Returns
        -------
        dict
            Summary with keys ``records``, ``pages_scraped``, ``output_file``.
        """
        url: str = task["url"]
        selectors: dict = task.get("selectors", {})
        paginate: bool = task.get("paginate", False)
        max_pages: int = task.get("max_pages", 10)
        output_format: str = task.get("output_format", "json")

        all_records: list[dict] = []
        pages_scraped = 0

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task_id = progress.add_task("Scraping...", total=None)

            async with BrowserEngine(headless=self.headless) as engine:
                current_url: str | None = url

                while current_url and pages_scraped < max_pages:
                    progress.update(
                        task_id,
                        description=f"[cyan]Page {pages_scraped + 1}[/cyan] -- {current_url[:60]}",
                    )

                    html = await self._fetch_with_retry(engine, current_url)
                    if html is None:
                        logger.warning("Failed to fetch %s after retries -- stopping.", current_url)
                        break

                    records = Scraper.extract(html, selectors)
                    all_records.extend(records)
                    pages_scraped += 1

                    if not paginate:
                        break

                    current_url = Scraper.next_page_url(html, current_url)
                    if current_url:
                        await asyncio.sleep(self.delay)

        output_file = await StorageManager.save(all_records, fmt=output_format)
        console.print(
            f"[green]Done![/green] Scraped [bold]{len(all_records)}[/bold] records "
            f"across [bold]{pages_scraped}[/bold] page(s). Saved to [italic]{output_file}[/italic]"
        )
        return {"records": len(all_records), "pages_scraped": pages_scraped, "output_file": str(output_file)}

    async def _fetch_with_retry(self, engine: BrowserEngine, url: str) -> str | None:
        page = await engine.new_page()
        for attempt in range(1, self.max_retries + 1):
            try:
                return await engine.fetch(page, url)
            except Exception as exc:
                logger.warning("Attempt %d/%d failed for %s: %s", attempt, self.max_retries, url, exc)
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
        await page.close()
        return None
