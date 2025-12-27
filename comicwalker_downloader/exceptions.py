class ComicWalkerError(Exception):
    """Base exception for ComicWalker downloader"""
    pass

class InvalidURLError(ComicWalkerError):
    """Invalid ComicWalker URL"""
    pass

class ParsingError(ComicWalkerError):
    """Failed to parse ComicWalker data"""
    pass

class DownloadError(ComicWalkerError):
    """Failed to download content"""
    pass

class EpisodeNotFoundError(ComicWalkerError):
    """Episode not found or unavailable"""
    pass