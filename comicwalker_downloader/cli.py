import sys
from loguru import logger
from typing import Optional
from comicwalker_downloader.comic_downloader import ComicDownloader
from comicwalker_downloader.comic_parser import ComicParser
from comicwalker_downloader.utils import is_valid_url
from comicwalker_downloader.exceptions import (
    ComicWalkerError,
    InvalidURLError
)
from comicwalker_downloader._version import __version__
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator
import os

class CLI:
    """ComicWalker Downloader CLI"""

    def download(
        self,
        url: str,
        episode: Optional[int] = None,
        output_dir: Optional[str] = None   
    ) -> None:
        try:
            if not is_valid_url(url):
                raise InvalidURLError(
                    "Invalid URL format. "
                    "Expected format: https://comic-walker.com/detail/KC_XXXXX_S"
                )
            
            logger.info("Fetching details...")
            parser = ComicParser(url=url)

            ep_list = parser.get_episode_list(only_active=True)
            current_ep = parser.get_current_episode()

            if not ep_list:
                logger.error("No episodes available for download")
                sys.exit(1)

            logger.success(f'✓ Found {len(ep_list)} episode(s) available for download')

            if episode is None:
                choices = [
                    Choice(
                        ep['number'],
                        name=f"[{ep['number']}] {ep['title']} {"<- CURRENT" if ep['number'] == current_ep['number'] else ""}"
                    ) for ep in ep_list
                ]
                episode = inquirer.select(
                    message="Select episode to download:",
                    choices=choices,
                    border=True,
                    default=current_ep['number'],
                ).execute()
            parser.set_episode(episode)
            
            if output_dir is None:
                output_dir = inquirer.filepath(
                    message="Select output directory:",
                    long_instruction="Leave as '.' to use the current directory",
                    default=".",
                    only_directories=True,
                    validate=PathValidator(is_dir=True),
                    transformer=lambda result: os.path.abspath(result) if result else os.getcwd(),
                ).execute()

            logger.info(f"Downloading episode {episode}...")
            ComicDownloader.run(parser, output_dir=output_dir)
            logger.success(f"✓ Finished! Saved to {os.path.abspath(output_dir)}")

        except ComicWalkerError as e:
            logger.error(f"{e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.debug(f"Error details:", exc_info=True)
            sys.exit(1)

    def check(
        self,
        url: str,
        show_inactive: bool = False
    ) -> None:
        try:
            if not is_valid_url(url):
                raise InvalidURLError(
                    "Invalid URL format. "
                    "Expected format: https://comic-walker.com/detail/KC_XXXXX_S"
                )
            
            logger.info("Fetching episodes...")
            parser = ComicParser(url=url)
            
            ep_list = parser.get_episode_list(only_active=not show_inactive)
            current_ep = parser.get_current_episode()
            
            if not ep_list:
                logger.warning("No episodes found")
                return
            
            logger.success(f"\nFound {len(ep_list)} episodes:\n")
            
            for ep in ep_list:
                status = "✓" if ep['is_active'] else "✗"
                current = " <- CURRENT" if ep['number'] == current_ep['number'] else ""
                print(f"{status} [{ep['number']}] {ep['title']}{current}")
                
        except ComicWalkerError as e:
            logger.error(f"{e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)
    
    def version(self) -> None:
        """Show version info"""
        print(f"comicwalker-downloader v{__version__}")