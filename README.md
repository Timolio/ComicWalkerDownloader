# ComicWalkerDownloader

ComicWalkerDownloader is a simple tool to download all images of a chapter from ComicWalker.

## Features

-   Downloads all images from the selected chapter.
-   Supports input of a chapter URL.
-   Allows choosing a specific chapter number or the current chapter.

## Installation

1. Ensure you have Python 3.8 or higher installed.

## Usage

1. Run the program with Python:
    ```bash
    python main.py
    ```
2. Enter the URL of any ComicWalker chapter.
3. Choose:
    - The chapter number you want to download.
    - Option to download the current chapter.
4. The images will be downloaded to the specified directory.

## Example Input

-   Paste a chapter URL, e.g., `https://comic-walker.com/detail/KC_006209_S/episodes/KC_0062090000700011_E?episodeType=latest`.
-   Specify the chapter number (e.g., `2`) or select the current one by pressing Enter.

## Notes

-   All downloaded images are saved in a separate folder named after the chapter, which is located inside a folder named after the manga title, in the same directory as the `comic_walker.py` file.
-   Make sure you do not use this tool to infringe any copyright laws.
