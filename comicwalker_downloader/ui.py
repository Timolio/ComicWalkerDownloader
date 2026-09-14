import os
import sys
from contextlib import contextmanager

from loguru import logger
from rich.console import Console
from rich.text import Text

from comicwalker_downloader.models import Episode, Rendition, Work

out = Console(markup=False, highlight=False)
err = Console(stderr=True, markup=False, highlight=False)

SPINNER = 'dots'

LOCKED_STYLE = '#6b7280'


def configure_logging(debug: bool = False) -> None:
    logger.remove()
    if debug:
        logger.add(sys.stderr, level='DEBUG')
        return
    logger.add(sys.stderr, format='{message}', level='INFO',
               filter=lambda record: record['level'].no < 30)
    logger.add(sys.stderr, format='<level>warning:</level> {message}', level='WARNING')


def error(message: str, hint: str | None = None) -> None:
    line = Text('error: ', style='red')
    line.append(message)
    err.print(line)
    if hint:
        err.print(' ' * 7 + hint)


def display_path(path: str) -> str:
    absolute = os.path.abspath(path)
    try:
        relative = os.path.relpath(absolute)
    except ValueError:
        return absolute
    return relative if not relative.startswith('..') else absolute


@contextmanager
def working(message: str):
    if out.is_terminal:
        with out.status(message, spinner=SPINNER):
            yield
    else:
        print(message, flush=True)
        yield


def work_header(work: Work) -> None:
    out.print()
    out.print(work.title, overflow='ellipsis', no_wrap=True)
    out.print(f'{len(work.episodes)} episodes, {len(work.active_episodes)} available')
    out.print()


def plural(count: int, noun: str) -> str:
    return f'{count} {noun}' if count == 1 else f'{count} {noun}s'


def episode_rows(work: Work) -> list[tuple[Episode | None, str]]:
    entries = []
    locked: list[Episode] = []

    def flush_locked():
        if not locked:
            return
        first, last = locked[0].number, locked[-1].number
        number = f'#{first}' if first == last else f'#{first}-{last}'
        entries.append((None, number, ''))
        locked.clear()

    for episode in work.episodes:
        if episode.is_active:
            flush_locked()
            entries.append((episode, f'#{episode.number}',
                            f"({plural(episode.page_count, 'page')})"))
        else:
            locked.append(episode)
    flush_locked()

    number_width = max((len(number) for _, number, _ in entries), default=0)
    pages_width = max((len(pages) for _, _, pages in entries), default=0)

    rows = []
    for episode, number, pages in entries:
        if episode is None:
            rows.append((None, f'{number:>{number_width}}  locked'))
        else:
            rows.append((episode, f'{number:>{number_width}}  '
                                  f'{pages:>{pages_width}}  {episode.title}'))
    return rows


def episode_table(work: Work) -> None:
    for episode, label in episode_rows(work):
        out.print(label, style=None if episode else LOCKED_STYLE)
    print()


def download_target(output_dir: str) -> None:
    out.print(f'Saving to {display_path(output_dir)}')


def saved(paths: list[str]) -> None:
    total = sum(os.path.getsize(path) for path in paths)
    out.print(f'Done. {total / 1e6:.1f} MB')


def describe_rendition(rendition: Rendition) -> str:
    return f'{rendition.width}x{rendition.height}'
