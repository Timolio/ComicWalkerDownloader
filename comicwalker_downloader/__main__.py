import os
import sys
import fire
from loguru import logger
from comicwalker_downloader.cli import CLI
from comicwalker_downloader.ui import configure_logging

def main() -> None: 
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')

    configure_logging(debug=bool(os.environ.get('COWADO_DEBUG')))

    argv = sys.argv[1:]
    if argv and 'comic-walker.com' in argv[0]:
        argv = ['download'] + argv  # cowado <url> == cowado download <url>

    try:
        fire.Fire(CLI, command=argv)
    except KeyboardInterrupt:
        logger.warning("Terminated by user")
        sys.exit(130)

if __name__ == "__main__":
    main()