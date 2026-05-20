"""Unit tests for openclaw.scraper."""

import pytest
from openclaw.scraper import Scraper

SIMPLE_HTML = """
<html>
  <body>
    <h1 class="title">Hello World</h1>
    <ul>
      <li class="item">Alpha</li>
      <li class="item">Beta</li>
      <li class="item">Gamma</li>
    </ul>
    <a href="/page/2">next</a>
  </body>
</html>
"""

PAGINATED_HTML = """
<html>
  <body>
    <p>Page content</p>
  </body>
</html>
"""


def test_extract_single_field():
    records = Scraper.extract(SIMPLE_HTML, {"title": "h1.title"})
    assert records == [{"title": "Hello World"}]


def test_extract_list_field():
    records = Scraper.extract(SIMPLE_HTML, {"items": "list:li.item"})
    assert records == [{"items": ["Alpha", "Beta", "Gamma"]}]


def test_next_page_url():
    url = Scraper.next_page_url(SIMPLE_HTML, "https://example.com/page/1")
    assert url == "https://example.com/page/2"


def test_next_page_none():
    url = Scraper.next_page_url(PAGINATED_HTML, "https://example.com/page/1")
    assert url is None
