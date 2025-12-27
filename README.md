<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/8fc8191c-79f2-4ca0-be3f-27c78389972c" />

CLI tool to download manga images from ComicWalker.

⚠️ **IMPORTANT:** Make sure you do not use this tool to infringe any copyright laws.

### Installation

**Python 3.8+** must be installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

### Usage

1. Copy the URL of any manga chapter, or specifically the one you want to download. Then run the command shown below.

```bash
cowado download [url]
# example
cowado download https://comic-walker.com/detail/KC_003002_S/episodes/KC_0030020011500011_E?episodeType=latest
```

2. After that, you can choose which chapter to download from all available options.

3. Next, enter the download path. You can also simply press Enter to download to the current directory.

🎉 The pages will then begin downloading in WebP format.

#### ► Direct Input Commands / Flags

You can skip the interactive part of the program by providing the necessary info with flags:

```bash
# Will start downloading immediately
cowado download [url] --episode=5 --output-dir="./manga"

# Will ask only for an output path
cowado download [url] --episode=1

# Will ask only to choose an episode
cowado download [url] --output-dir="."
```

#### ► Check Available Episodes

View all available episodes without downloading:

```bash
cowado check [url]

# Show inactive episodes as well
cowado check [url] --show-inactive
```

#### ► Other Commands

```bash
# Show version
cowado version
```
