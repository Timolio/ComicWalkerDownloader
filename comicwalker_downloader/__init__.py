"""
comicwalker_downloader
======================

A Python package for scraping and downloading manga chapters and images from ComicWalker.
"""

from .parser import fetch_work, parse_work
from .models import Episode, Page, Rendition, Work
from .downloader import ComicDownloader
from .exceptions import (
    ComicWalkerError,
    DownloadError,
    EpisodeNotFoundError,
    InvalidURLError,
    NetworkError,
    ParsingError,
)
from ._version import __version__

__all__ = [
    "fetch_work",
    "parse_work",
    "ComicDownloader",
    "Work",
    "Episode",
    "Page",
    "Rendition",
    "ComicWalkerError",
    "NetworkError",
    "ParsingError",
    "DownloadError",
    "InvalidURLError",
    "EpisodeNotFoundError",
    "__version__",
]