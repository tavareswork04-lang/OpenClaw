# OpenClaw

> Async web scraping and browser automation agent — powered by Playwright and BeautifulSoup4.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Async-first** — built on `asyncio` and Playwright for high-throughput scraping
- **CSS selector engine** — simple declarative config for any page structure
- **Auto-pagination** — follows `next` links automatically
- **Multiple output formats** — JSON and CSV with timestamped filenames
- **Retry logic** — exponential back-off on transient failures
- **Rich terminal UI** — progress spinners and coloured summaries

## Installation

```bash
git clone https://github.com/tavareswork04-lang/OpenClaw.git
cd OpenClaw
pip install -e .
playwright install chromium
```

## Quick Start

```python
import asyncio
from openclaw.agent import OpenClawAgent

async def main():
    agent = OpenClawAgent(headless=True)
    result = await agent.run({
        "url": "https://books.toscrape.com/catalogue/page-1.html",
        "selectors": {
            "__container__": "article.product_pod",
            "title": "h3 a",
            "price": "p.price_color",
        },
        "paginate": True,
        "max_pages": 5,
        "output_format": "json",
    })
    print(result)

asyncio.run(main())
```

## Project Structure

```
OpenClaw/
├── openclaw/
│   ├── __init__.py      # Public API
│   ├── agent.py         # Orchestrator
│   ├── browser.py       # Playwright engine
│   ├── scraper.py       # HTML extraction
│   ├── storage.py       # Async file output
│   └── utils.py         # Logger & helpers
├── tests/
│   └── test_scraper.py
├── examples/
│   └── basic_scrape.py
├── docs/
│   └── quickstart.md
├── requirements.txt
├── setup.py
└── README.md
```

## Tests

```bash
pytest tests/ -v
```

## License

MIT — see [LICENSE](LICENSE).
