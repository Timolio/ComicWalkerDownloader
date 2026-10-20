<!-- i18readme -->
**English** | [Русский](translations/README.ru.md) | [中文](translations/README.zh.md)
<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.11%20%7C%203.12%20%7C%203.13%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

CLI tool to download manga images from [ComicWalker](https://comic-walker.com).

> ⚠️ Make sure you do not use this tool to infringe any copyright laws.

---

### Installation

**Python 3.11+** is required. Download it from [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

---

### Quick start

Paste any ComicWalker link and pick an episode:

```bash
cowado https://comic-walker.com/detail/KC_000097_S
```

```
逢魔暮らしの奴さん
24 episodes, 5 available

? Episode
      #1  (13 pages)  第1話
      #2  (10 pages)  第2話
    ❯ #3   (8 pages)  第3話
   #4-15  locked
     #16    (1 page)  1巻発売記念イラスト

? Size  1284x1844

Saving to 逢魔暮らしの奴さん/003
████████████████████████████  8/8
Done. 1.2 MB
```

That is the whole flow: choose an episode, choose an image size, wait.

Any ComicWalker URL works — a series page or a direct episode link, with or without query parameters:

```bash
cowado https://comic-walker.com/detail/KC_000097_S
cowado https://comic-walker.com/detail/KC_000097_S?episodeType=first
cowado https://comic-walker.com/detail/KC_000097_S/episodes/KC_0000970000100011_E
```

---

### Reading the episode list

```
    #1  (13 pages)  第1話
 #4-15  locked
   #16    (1 page)  1巻発売記念イラスト
```

- **`#1`** is the episode number. Pass it as `--episode=1` to skip the prompt and download that episode right away.
- **`#4-15  locked`** means episodes 4 through 15 are not free right now. They are shown so you can see what exists, but they cannot be selected.
- Some entries are not chapters at all — illustrations or announcements. The page count gives them away.

---

### Commands

#### `cowado <url>`

Short form of `cowado download <url>`. Both do the same thing.

#### `cowado check <url>`

Show the episode list without downloading anything.

```bash
cowado check https://comic-walker.com/detail/KC_000097_S
```

```
逢魔暮らしの奴さん
24 episodes, 5 available

    #1  (13 pages)  第1話
    #2  (10 pages)  第2話
    #3   (8 pages)  第3話
 #4-15  locked
   #16    (1 page)  1巻発売記念イラスト
#17-23  locked
   #24   (8 pages)  第22話
```

#### `cowado version`

```bash
cowado version
```

---

### Flags

| Flag                    | What it does                                                       |
| ----------------------- | ------------------------------------------------------------------ |
| `--episode=N`           | Download episode N without asking                                  |
| `--size=max`            | Pick the image size without asking: `max`, `min`, `mobile`, `desktop` |
| `--output_dir="./path"` | Save somewhere else (default: `{manga title}/{episode number}/`)    |

```bash
# no questions asked
cowado <url> --episode=5 --size=max --output_dir="./manga"
```

### Batch downloads

Use `--all` to download all available episodes in the fetched episode list, or
`--episodes` to select numbers and inclusive ranges. These flags cannot be
combined with each other or with `--episode`.

```bash
cowado <url> --all --output_dir="./manga"
cowado <url> --episodes="1-5,8,10-12" --size=max
```

Batch downloads skip unavailable episodes, remove repeated selections and run in
episode-number order. An empty selection is an error. Unless `--size` is given,
batch downloads use `max` without prompting. A download failure stops the batch.

Each episode gets its own numbered folder: by default `{manga title}/001/`,
`{manga title}/002/`, etc. With `--output_dir="./manga"`, these become
`./manga/001/`, `./manga/002/`, etc., even when the batch selects only one episode.
Invalid or duplicate episode numbers are rejected before downloading to prevent
folder collisions. Existing files at the same paths may be overwritten, as in
single-episode downloads.

The existing single-episode download behavior, including custom output directories,
is unchanged.

**About `--size`.** ComicWalker serves two image sizes, and which one is larger depends on the title. `max` and `min` always pick by actual size, so they are the safe choice for scripts. `mobile` is always 768 px wide; `desktop` is capped by height and can land anywhere between 650 and 1284 px.

---

### Where the files go

```
逢魔暮らしの奴さん/
└── 003/
    ├── 001.webp
    ├── 002.webp
    └── ...
```

One folder per episode, pages named by number. Use `--output_dir` to change the location.

---

### Troubleshooting

Set `COWADO_DEBUG=1` to see full error details instead of a one-line message.

```bash
COWADO_DEBUG=1 cowado <url>
```

## Star History

[![Star History Chart](https://api.star-history.com/image?repos=Timolio/ComicWalkerDownloader&type=date&legend=top-left)](https://www.star-history.com/?repos=Timolio%2FComicWalkerDownloader&type=date&legend=top-left)
