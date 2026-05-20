"""OpenClaw — async web scraping and automation agent."""

from openclaw.agent import OpenClawAgent
from openclaw.browser import BrowserEngine
from openclaw.scraper import Scraper

__version__ = "0.1.0"
__all__ = ["OpenClawAgent", "BrowserEngine", "Scraper"]
