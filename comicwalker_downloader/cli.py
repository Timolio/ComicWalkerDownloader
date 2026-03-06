import sys
import os
from loguru import logger
from typing import Optional
from comicwalker_downloader.comic_downloader import ComicDownloader
from comicwalker_downloader.comic_parser import ComicParser
from comicwalker_downloader.utils import is_valid_url, sanitize_dirname
from comicwalker_downloader.exceptions import (
    ComicWalkerError,
    InvalidURLError,
    EpisodeNotFoundError
)
from comicwalker_downloader._version import __version__
from InquirerPy import inquirer
from InquirerPy.base.control import Choice


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

            work_title = parser.get_work_title()
            ep_list = parser.get_episode_list(only_active=True)

            if not ep_list:
                logger.error("No episodes available for download")
                sys.exit(1)

            print(f"\n  {work_title}")
            print(f"  {'─' * len(work_title)}")
            print(f"  {len(ep_list)} episode(s) available\n")

            if episode is not None:
                parser.set_episode(episode)
            else:
                current_ep = parser.get_current_episode()
                choices = [
                    Choice(
                        ep['number'],
                        name=f"[{ep['number']}] {ep['title']}{'  ← CURRENT' if ep['number'] == current_ep['number'] else ''}"
                    ) for ep in ep_list
                ]
                selected = inquirer.select(
                    message="Select episode to download:",
                    choices=choices,
                    border=True,
                    default=current_ep['number'],
                ).execute()
                parser.set_episode(selected)

            ep_no = parser.ep['internal']['episodeNo']
            ep_title = parser.ep['title']

            if output_dir is None:
                output_dir = os.path.join(sanitize_dirname(work_title), f'{ep_no:03d}')

            print(f"\n  Downloading → [{ep_no}] {ep_title}")
            print(f"  Saving to   → {os.path.abspath(output_dir)}\n")

            ComicDownloader.run(parser, output_dir=output_dir)
            logger.success(f"✓ Done! {os.path.abspath(output_dir)}")

        except EpisodeNotFoundError as e:
            logger.error(f"{e}")
            logger.info("Use 'cowado check <url>' to see available episodes")
            sys.exit(1)
        except ComicWalkerError as e:
            logger.error(f"{e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.debug("Error details:", exc_info=True)
            sys.exit(1)

    def check(
        self,
        url: str,
    ) -> None:
        try:
            if not is_valid_url(url):
                raise InvalidURLError(
                    "Invalid URL format. "
                    "Expected format: https://comic-walker.com/detail/KC_XXXXX_S"
                )

            logger.info("Fetching details...")
            parser = ComicParser(url=url)

            work_title = parser.get_work_title()
            ep_list = parser.get_episode_list(only_active=False)
            current_ep = parser.get_current_episode()

            print(f"\n  {work_title}")
            print(f"  {'─' * len(work_title)}\n")

            if not ep_list:
                logger.warning("No episodes found")
                return

            for ep in ep_list:
                status = "✓" if ep['is_active'] else "✗"
                current = "  ← CURRENT" if ep['number'] == current_ep['number'] else ""
                locked = "  (locked)" if not ep['is_active'] else ""
                print(f"  {status}  [{ep['number']}] {ep['title']}{locked}{current}")

            active_count = sum(1 for ep in ep_list if ep['is_active'])
            total_count = len(ep_list)
            print(f"\n  {total_count} episode(s) total · {active_count} available\n")

        except ComicWalkerError as e:
            logger.error(f"{e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.debug("Error details:", exc_info=True)
            sys.exit(1)

    def version(self) -> None:
        """Show version info"""
        print(f"comicwalker-downloader v{__version__}")
