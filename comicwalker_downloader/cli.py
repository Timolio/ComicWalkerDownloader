import os
import sys

from loguru import logger
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.utils import get_style

from comicwalker_downloader import ui
from comicwalker_downloader.api import DESKTOP_SIZE_TYPE, MOBILE_SIZE_TYPE, make_session
from comicwalker_downloader.downloader import ComicDownloader
from comicwalker_downloader.models import Episode, Rendition, Work
from comicwalker_downloader.parser import fetch_work
from comicwalker_downloader.utils import is_valid_url, sanitize_dirname
from comicwalker_downloader.exceptions import (
    ComicWalkerError,
    EpisodeNotFoundError,
    InvalidURLError,
)
from comicwalker_downloader._version import __version__


def fail(error: Exception) -> None:
    if isinstance(error, EpisodeNotFoundError):
        ui.error(str(error), "run 'cowado check <url>' to see what is available")
    elif isinstance(error, ComicWalkerError):
        ui.error(str(error))
    else:
        ui.error(f'unexpected error: {error}')
        logger.debug('Error details:', exc_info=True)
    sys.exit(1)


def check_url(url: str) -> None:
    if not is_valid_url(url):
        raise InvalidURLError(
            'Invalid URL. Expected https://comic-walker.com/detail/KC_XXXXX_S'
        )


class CLI:
    """ComicWalker Downloader"""

    def download(
        self,
        url: str,
        episode: int | None = None,
        output_dir: str | None = None,
        size: str | None = None
    ) -> None:
        session = make_session()
        try:
            check_url(url)

            if size is not None:
                size = str(size)

            with ui.working('Fetching episodes'):
                work = fetch_work(url, session)

            if not work.active_episodes:
                raise ComicWalkerError('No episodes available for download')

            ui.work_header(work)

            chosen = self._select_episode(work, episode)
            output_dir = self._resolve_output_dir(work, chosen, output_dir)

            downloader = ComicDownloader(session)
            with ui.working('Checking sizes'):
                renditions = downloader.list_renditions(chosen)
            rendition = self._select_rendition(renditions, size)

            ui.download_target(output_dir)
            paths = downloader.run(chosen, output_dir=output_dir, rendition=rendition)
            ui.saved(paths)
        except Exception as error:
            fail(error)
        finally:
            session.close()

    def check(self, url: str) -> None:
        session = make_session()
        try:
            check_url(url)

            with ui.working('Fetching'):
                work = fetch_work(url, session)

            ui.work_header(work)
            if not work.episodes:
                logger.warning('No episodes found')
                return
            ui.episode_table(work)
        except Exception as error:
            fail(error)
        finally:
            session.close()

    def version(self) -> None:
        """Show version info"""
        print(f'cowado {__version__}')

    def _select_episode(self, work: Work, number: int | None) -> Episode:
        if number is None:
            choices = [
                Choice(episode.number, name=label) if episode else Separator(label)
                for episode, label in ui.episode_rows(work)
            ]
            available = [ep.number for ep in work.active_episodes]
            current = work.current_episode
            preferred = current.number if current is not None else None
            number = inquirer.select(
                message='Episode',
                choices=choices,
                default=preferred if preferred in available else available[0],
                style=get_style({'separator': ui.LOCKED_STYLE}, style_override=False),
            ).execute()

        episode = work.find_episode(number)
        if episode is None:
            raise EpisodeNotFoundError(f'Episode {number} not found or not available')
        return episode

    def _select_rendition(self, renditions: list[Rendition], size: str | None) -> Rendition:
        if not renditions:
            raise ComicWalkerError('No images available for this episode')
        if size is not None:
            return self._rendition_by_name(renditions, size)
        if len(renditions) == 1:
            return renditions[0]

        selected = inquirer.select(
            message='Size',
            choices=[Choice(r.size_type, name=ui.describe_rendition(r)) for r in renditions],
            default=renditions[0].size_type,
        ).execute()
        return next(r for r in renditions if r.size_type == selected)

    @staticmethod
    def _rendition_by_name(renditions: list[Rendition], size: str) -> Rendition:
        wanted = size.strip().lower()
        if wanted == 'max':
            return renditions[0]
        if wanted == 'min':
            return renditions[-1]

        tokens = {'mobile': MOBILE_SIZE_TYPE, 'desktop': DESKTOP_SIZE_TYPE}
        if wanted in tokens:
            for rendition in renditions:
                if rendition.size_type == tokens[wanted]:
                    return rendition
            raise ComicWalkerError(f'This episode has no {wanted} size')
        raise ComicWalkerError(
            f'Unknown size {size!r}. Use max, min, mobile or desktop'
        )

    @staticmethod
    def _resolve_output_dir(work: Work, episode: Episode, output_dir: str | None) -> str:
        if output_dir is not None:
            return output_dir
        return os.path.join(sanitize_dirname(work.title), f'{episode.number:03d}')
