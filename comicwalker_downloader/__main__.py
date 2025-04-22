import fire
from comicwalker_downloader.run import run

def main() -> None: 
    try:
        fire.Fire(run)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()