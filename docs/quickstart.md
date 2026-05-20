# OpenClaw — Quick Start

## Installation

```bash
pip install -e .
playwright install chromium
```

## Minimal example

```python
import asyncio
from openclaw.agent import OpenClawAgent

async def main():
    agent = OpenClawAgent()
    result = await agent.run({
        "url": "https://books.toscrape.com",
        "selectors": {
            "__container__": "article.product_pod",
            "title": "h3 a",
            "price": "p.price_color",
        },
        "output_format": "json",
    })
    print(result)

asyncio.run(main())
```

## Selector syntax

| Syntax | Behaviour |
|---|---|
| `"css-selector"` | First match, text content |
| `"list:css-selector"` | All matches, list of strings |
| `"__container__"` | Iterate over repeating elements |

## Pagination

Set `paginate: True` and optionally `max_pages` to follow **next** links automatically.

## Output formats

`output_format` accepts `"json"` (default) or `"csv"`. Files land in `./output/`.
