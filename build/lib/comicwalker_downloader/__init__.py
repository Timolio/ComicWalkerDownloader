from .comic_parser import ComicParser
from .comic_downloader import ComicDownloader

def fetch_episode_list(url: str):
    parser = ComicParser(url)
    return parser.get_cli_list()

def download_episode(url: str, episode_number: int = None, output_dir: str = '.'):
    parser = ComicParser(url)
    parser.set_episode(episode_number)
    ComicDownloader.run(parser, output_dir=output_dir)