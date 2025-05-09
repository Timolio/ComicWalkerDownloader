import os
import requests
from tqdm import tqdm
from comicwalker_downloader.comic_parser import ComicParser
from loguru import logger

class ComicDownloader:
    @staticmethod
    def run(parser: ComicParser, output_dir: str = '.') -> None:
        ComicDownloader._fetch_episode(parser.ep, output_dir)
    
    @staticmethod
    def _fetch_episode(ep: dict, output_dir: str) -> None:
        try:
            response = requests.get(
                f'https://comic-walker.com/api/contents/viewer?episodeId={ep['id']}&imageSizeType=width%3A768',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            raise e

        if not data.get("manuscripts"):
            logger.error(f"No pages available for the chapter")
            raise

        os.makedirs(output_dir, exist_ok=True)
        
        for page in tqdm(data["manuscripts"], desc=f"Downloading pages...", unit="page", colour="CYAN"):
            ComicDownloader._download_page(page, output_dir)

    @staticmethod
    def _download_page(page: dict, output_dir: str) -> None:
        try:
            drm_hash = bytes.fromhex(page["drmHash"])
            response = requests.get(page["drmImageUrl"], stream=True)
            response.raise_for_status()

            encrypted_data = response.content
            decrypted_data = bytes([b ^ drm_hash[i % len(drm_hash)] for i, b in enumerate(encrypted_data)])

            file_path = os.path.join(output_dir, f'{page["page"]}.webp')
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
        except Exception as e:
            raise e