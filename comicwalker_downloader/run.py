import fire
from loguru import logger
from comicwalker_downloader.utils import is_valid_url
from comicwalker_downloader.comic_parser import ComicParser
from comicwalker_downloader.comic_downloader import ComicDownloader

def run(url: str) -> None:
    try:
        if not is_valid_url(url):
            logger.error(f"Invalid URL: {url}")
            return
        
        logger.info("Fetching details...")
        parser = ComicParser(url=url)

        cli_list = parser.get_cli_list()
        print(f'\nFound {len(cli_list)} episodes:\n')

        print("\n".join(cli_list))
        
        chapter_number = None 

        inp = input("\n\nDownload the current one? [yes/no]")
        if inp.lower() not in ['yes', 'y']:
            inp = input("\nEnter the chapter number: ")
            chapter_number = int(inp) if inp else None

        parser.set_episode(chapter_number)
        ComicDownloader.run(parser)

        logger.info("✓ Finished")
    except Exception as e:
        logger.error(e)

if __name__ == "__main__":
    fire.Fire(run)