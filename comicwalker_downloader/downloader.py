import os
import requests
from concurrent.futures import ThreadPoolExecutor
from rich.progress import BarColumn, Progress, TextColumn
from comicwalker_downloader.api import IMAGE_SIZE_TYPES, TIMEOUT, VIEWER_URL
from comicwalker_downloader.exceptions import ComicWalkerError, DownloadError, NetworkError, ParsingError
from comicwalker_downloader.models import Episode, Page, Rendition
from loguru import logger

MAX_WORKERS = 6

class ComicDownloader:
    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def list_renditions(self, episode: Episode) -> list[Rendition]:
        found: dict[tuple[int, int], Rendition] = {}
        for size_type in IMAGE_SIZE_TYPES:
            try:
                rendition = self._fetch_viewer(episode, size_type)
            except DownloadError:
                continue
            key = (rendition.width, rendition.height)
            if key not in found:
                found[key] = rendition
        return sorted(found.values(), key=lambda r: r.pixels, reverse=True)

    def _fetch_viewer(self, episode: Episode, size_type: str) -> Rendition:
        try:
            response = self.session.get(
                VIEWER_URL,
                params={'episodeId': episode.id, 'imageSizeType': size_type},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout as e:
            raise NetworkError("Timed out fetching episode data") from e
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else '?'
            raise DownloadError(f"Episode data unavailable (HTTP {status})") from e
        except requests.exceptions.JSONDecodeError as e:
            raise ParsingError("Episode data is not valid JSON") from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to fetch episode data: {e}") from e

        rendition = Rendition.from_api(size_type, data)
        if not rendition.pages:
            raise DownloadError("No images available for this episode")
        return rendition

    def run(self, episode: Episode, rendition: Rendition, output_dir: str = '.') -> list[str]:
        if rendition.is_stale:
            logger.info("Image links expired, refreshing...")
            rendition = self._fetch_viewer(episode, rendition.size_type)

        pages = rendition.pages
        os.makedirs(output_dir, exist_ok=True)

        def download_one(page: Page) -> str | None:
            try:
                return self._download_page(page, output_dir)
            except ComicWalkerError as e:
                logger.warning(f"Failed to download page {page.number}: {e}")
                return None

        paths = []
        columns = [BarColumn(bar_width=None), TextColumn('{task.completed}/{task.total}')]
        with Progress(*columns) as bar, ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            task = bar.add_task('', total=len(pages))
            for path in pool.map(download_one, pages):
                paths.append(path)
                bar.advance(task)

        failed = [page.number for page, path in zip(pages, paths) if path is None]
        if failed:
            raise DownloadError(
                f"Failed to download {len(failed)} page(s): "
                f"{', '.join(str(number) for number in failed)}"
            )

        return paths

    @staticmethod
    def _decrypt(data: bytes, key: bytes) -> bytes:
        if not data:
            return data
        repeated = (key * (len(data) // len(key) + 1))[:len(data)]
        return (int.from_bytes(data, 'big') ^ int.from_bytes(repeated, 'big')).to_bytes(len(data), 'big')

    def _download_page(self, page: Page, output_dir: str) -> str:
        if not page.drm_hash or not page.image_url or page.number is None:
            raise DownloadError(f"Missing data for page {page.number}: cannot decrypt image")

        try:
            drm_hash = bytes.fromhex(page.drm_hash)
        except ValueError as e:
            raise DownloadError(f"Invalid DRM hash for page {page.number}") from e

        try:
            response = self.session.get(page.image_url, timeout=TIMEOUT)
            response.raise_for_status()
            encrypted_data = response.content
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Timed out downloading page {page.number}") from e
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to download image for page {page.number}: {e}") from e

        decrypted_data = self._decrypt(encrypted_data, drm_hash)

        file_path = os.path.join(output_dir, f'{page.number:03d}.webp')

        try:
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
        except OSError as e:
            raise DownloadError(f"Failed to save page {page.number}: {e}") from e

        return file_path
