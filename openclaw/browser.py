"""Playwright-based async browser engine."""

from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.async_api import async_playwright, Browser, Page, Playwright

from openclaw.utils import get_logger

if TYPE_CHECKING:
    pass

logger = get_logger()


class BrowserEngine:
    """Async context manager wrapping a Playwright browser instance.

    Usage
    -----
    ::

        async with BrowserEngine(headless=True) as engine:
            page = await engine.new_page()
            html = await engine.fetch(page, "https://example.com")
    """

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    async def __aenter__(self) -> "BrowserEngine":
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        logger.debug("Browser launched (headless=%s)", self.headless)
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.debug("Browser closed.")

    async def new_page(self) -> Page:
        """Open and return a new browser page."""
        assert self._browser is not None, "BrowserEngine not started — use as async context manager."
        return await self._browser.new_page()

    async def fetch(self, page: Page, url: str, wait_for: str = "networkidle") -> str:
        """Navigate *page* to *url* and return the page HTML.

        Parameters
        ----------
        page:
            An open Playwright ``Page`` object.
        url:
            Target URL.
        wait_for:
            Playwright ``wait_until`` event (default: ``"networkidle"``).
        """
        logger.debug("Fetching %s", url)
        await page.goto(url, wait_until=wait_for, timeout=30_000)
        return await page.content()

    async def screenshot(self, page: Page, path: str = "screenshot.png") -> None:
        """Save a screenshot of *page* to *path*."""
        await page.screenshot(path=path, full_page=True)
        logger.info("Screenshot saved to %s", path)
