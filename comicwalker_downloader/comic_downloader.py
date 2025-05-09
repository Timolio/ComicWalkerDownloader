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
            url = f'https://comic-walker.com/api/contents/viewer?episodeId={ep['id']}&imageSizeType=width%3A768'
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }
            )
            response.raise_for_status()
            data = response.json()
        except Exception as ex:
            raise ValueError(f"Failed to fetch ComicWalker viewer API: {ex}")
            
        
        manuscripts = data.get("manuscripts")
        if not manuscripts:
            raise ValueError("No images available for this episode")

        os.makedirs(output_dir, exist_ok=True)
        paths = []
        for page in tqdm(manuscripts, desc=f"Downloading", unit="page", colour="CYAN"):
            try:
                path = ComicDownloader._download_page(page, output_dir)
                paths.append(path)
            except Exception as e:
                raise ValueError(f"Failed to download page {page.get('page')}: {e}")
        return paths

    @staticmethod
    def _download_page(page: dict, output_dir: str) -> None:
        drm_hash_hex = page.get("drmHash")
        image_url = page.get("drmImageUrl")
        page_idx = page.get("page")

        if not drm_hash_hex or not image_url or not page_idx:
            raise ValueError("Missing essential page info for decryption")
        
        drm_hash = bytes.fromhex(drm_hash_hex)
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        encrypted_data = response.content
        decrypted_data = bytes([b ^ drm_hash[i % len(drm_hash)] for i, b in enumerate(encrypted_data)])

        file_path = os.path.join(output_dir, f'{page_idx}.webp')
        with open(file_path, "wb") as f:
            f.write(decrypted_data)
        return file_path