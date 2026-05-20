"""Basic scraping example -- books.toscrape.com."""

import asyncio
from openclaw.agent import OpenClawAgent


async def main() -> None:
    agent = OpenClawAgent(headless=True, delay=1.5)

    result = await agent.run(
        {
            "url": "https://books.toscrape.com/catalogue/page-1.html",
            "selectors": {
                "__container__": "article.product_pod",
                "title": "h3 a",
                "price": "p.price_color",
                "rating": "p.star-rating",
                "availability": "p.availability",
            },
            "paginate": True,
            "max_pages": 3,
            "output_format": "json",
        }
    )

    print(f"Done! {result['records']} books scraped from {result['pages_scraped']} pages.")
    print(f"Output: {result['output_file']}")


if __name__ == "__main__":
    asyncio.run(main())
