import os
import requests
from tqdm import tqdm
from comicwalker_downloader.comic_parser import ComicParser
from comicwalker_downloader.exceptions import DownloadError
from loguru import logger
from typing import List

class ComicDownloader:
    @staticmethod
    def run(parser: ComicParser, output_dir: str = '.') -> List[str]:
        return ComicDownloader._fetch_episode(parser.ep, output_dir)
    
    @staticmethod
    def _fetch_episode(ep: dict, output_dir: str) -> List[str]:
        try:
            url = f"https://comic-walker.com/api/contents/viewer?episodeId={ep['id']}&imageSizeType=width%3A768"
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise DownloadError(f"Failed to fetch episode data: {e}")
            
        manuscripts = data.get("manuscripts")
        if not manuscripts:
            raise DownloadError("No images available for this episode")

        os.makedirs(output_dir, exist_ok=True)
        paths = []

        failed_pages = []
        for page in tqdm(manuscripts, unit="page", colour="CYAN"):
            try:
                path = ComicDownloader._download_page(page, output_dir)
                paths.append(path)
            except Exception as e:
                page_num = page.get("page", "?")
                failed_pages.append(page_num)
                logger.warning(f"Failed to download page {page_num}: {e}")
        
        if failed_pages:
            raise DownloadError(
                f"Failed to download {len(failed_pages)} page(s): {', '.join(map(str, failed_pages))}"
            )
        
        return paths

    @staticmethod
    def _download_page(page: dict, output_dir: str) -> str:
        drm_hash_hex = page.get("drmHash")
        image_url = page.get("drmImageUrl")
        page_idx = page.get("page")

        if not drm_hash_hex or not image_url or not page_idx:
            raise DownloadError(f"Missing data for page {page_idx}: cannot decrypt image")
        
        try:
            drm_hash = bytes.fromhex(drm_hash_hex)
        except ValueError:
            raise DownloadError(f"Invalid DRM hash for page {page_idx}")

        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            encrypted_data = response.content
        except requests.exceptions.RequestException as e:
            raise DownloadError(f"Failed to download image for page {page_idx}: {e}")
        
        decrypted_data = bytes([b ^ drm_hash[i % len(drm_hash)] for i, b in enumerate(encrypted_data)])

        file_path = os.path.join(output_dir, f'{page_idx:03d}.webp')

        try:
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
        except IOError as e:
            raise DownloadError(f"Failed to save page {page_idx}: {e}")
        
        return file_path
