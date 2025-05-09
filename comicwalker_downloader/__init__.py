"""
comicwalker_downloader
======================

A Python package for scraping and downloading manga chapters and images from ComicWalker.
"""

from .comic_parser import ComicParser
from .comic_downloader import ComicDownloader

__all__ = ["ComicParser", "ComicDownloader"]