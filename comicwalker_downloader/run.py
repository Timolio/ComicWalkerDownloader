import fire
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator
from loguru import logger
from comicwalker_downloader.utils import is_valid_url
from comicwalker_downloader.comic_parser import ComicParser
from comicwalker_downloader.comic_downloader import ComicDownloader
import sys

def run(url: str) -> None:
    try:
        if not is_valid_url(url):
            logger.error(f"Invalid URL: {url}")
            sys.exit(1)
        
        logger.info("Fetching details...")
        parser = ComicParser(url=url)
        ep_list = parser.get_episode_list()
        current_ep = parser.get_current_episode()
        logger.info(f'Found {len(ep_list)} episodes...')
        ep_list = parser.get_episode_list(only_active=True)
        logger.success(f'✓ Found {len(ep_list)} episodes available for download...')

        choices = [Choice(ep['number'], name=ep['title']) for ep in ep_list]
        episode_number = inquirer.select(
            message="Select episode to download:",
            long_instruction="The current episode is selected by default",
            choices=choices,
            border=True,
            default=current_ep['number'],
        ).execute()
        
        output_dir = inquirer.filepath(
            message="Select output directory:",
            long_instruction="Leave as it is to use the current directory",
            default=".",
            only_directories=True,
            validate=PathValidator(is_dir=True),
            transformer=lambda result: os.path.abspath(result) if result else os.getcwd(),
        ).execute()

        parser.set_episode(episode_number)
        ComicDownloader.run(parser, output_dir=output_dir)

        logger.success("✓ Finished")
    except Exception as e:
        logger.error(e)
        sys.exit(1)

if __name__ == "__main__":
    fire.Fire(run)