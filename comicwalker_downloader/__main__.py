import fire
from loguru import logger
from comicwalker_downloader.cli import CLI

def main() -> None: 
    try:
        fire.Fire(CLI)
    except KeyboardInterrupt:
        logger.warning("Terminated by user")

if __name__ == "__main__":
    main()