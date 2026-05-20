"""HTML extraction logic using BeautifulSoup4."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from openclaw.utils import get_logger

logger = get_logger()


class Scraper:
    """Static methods for extracting structured data from HTML."""

    @staticmethod
    def extract(html: str, selectors: dict[str, str]) -> list[dict[str, Any]]:
        """Extract data from *html* using CSS *selectors*.

        Selector conventions
        --------------------
        - ``"css-selector"`` — extract text of the **first** match.
        - ``"list:css-selector"`` — extract text of **all** matches as a list.
        - ``__container__`` key — iterate over each container element and
          apply the remaining selectors within it.

        Parameters
        ----------
        html:
            Raw HTML string.
        selectors:
            Mapping of field name to CSS selector string.

        Returns
        -------
        list[dict]
            Extracted records.
        """
        soup = BeautifulSoup(html, "lxml")

        if "__container__" not in selectors:
            record = Scraper._extract_fields(soup, selectors)
            return [record] if record else []

        container_sel = selectors["__container__"]
        field_sels = {k: v for k, v in selectors.items() if k != "__container__"}
        records = []
        for container in soup.select(container_sel):
            record = Scraper._extract_fields(container, field_sels)
            if record:
                records.append(record)
        return records

    @staticmethod
    def _extract_fields(
        scope: BeautifulSoup | Any,
        selectors: dict[str, str],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for field, selector in selectors.items():
            if selector.startswith("list:"):
                css = selector[len("list:"):]
                result[field] = [el.get_text(strip=True) for el in scope.select(css)]
            else:
                el = scope.select_one(selector)
                result[field] = el.get_text(strip=True) if el else None
        return result

    @staticmethod
    def next_page_url(html: str, current_url: str) -> str | None:
        """Find the next-page URL from *html*, relative to *current_url*.

        Looks for common pagination patterns:
        - ``<a rel="next">``
        - ``<a>`` whose text matches next / > / >>
        - ``<link rel="next">``

        Returns ``None`` when no next page is detected.
        """
        soup = BeautifulSoup(html, "lxml")
        base = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(current_url))

        # 1. <link rel="next">
        link_next = soup.find("link", rel="next")
        if link_next and link_next.get("href"):
            return urljoin(base, link_next["href"])

        # 2. <a rel="next">
        a_rel_next = soup.find("a", rel="next")
        if a_rel_next and a_rel_next.get("href"):
            return urljoin(base, a_rel_next["href"])

        # 3. <a> with next-like text
        next_pattern = re.compile(r"^(next|>|>>)$", re.IGNORECASE)
        for a in soup.find_all("a", href=True):
            if next_pattern.match(a.get_text(strip=True)):
                return urljoin(base, a["href"])

        return None
