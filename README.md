<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

CLI tool to download manga images from [ComicWalker](https://comic-walker.com).

> ⚠️ Make sure you do not use this tool to infringe any copyright laws.

---

### Installation

**Python 3.8+** is required. Download it from [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

---

### Usage

#### `cowado download <url>`

Pass any ComicWalker URL — a series page, a direct episode link, or one with query params:

```bash
cowado download https://comic-walker.com/detail/KC_008483_S
cowado download https://comic-walker.com/detail/KC_008483_S?episodeType=first
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E?episodeType=latest
...
```

The tool fetches the manga details and shows you what it found:

```
  青春ヒストリカ
  ────────────────
  12 episode(s) available

? Select episode to download:
 ❯ [12] 第12話  ← CURRENT
   [11] 第11話
   [10] 第10話
   ...

  Downloading → [12] 第12話
  Saving to   → /home/user/青春ヒストリカ/012/

  ████████████████████████  22/22 pages

  ✓ Done! /home/user/青春ヒストリカ/012/
```

Pages are saved as `.webp` files, named by page number (`001.webp`, `002.webp`, ...).

---

#### Flags

| Flag                    | Description                                                                |
| ----------------------- | -------------------------------------------------------------------------- |
| `--episode=N`           | Skip selection and download episode N directly                             |
| `--output_dir="./path"` | Override the output directory (default: `{manga title}/{episode number}/`) |

```bash
# Download episode 5 directly to a custom folder
cowado download <url> --episode=5 --output_dir="./manga"
```

---

#### `cowado check <url>`

Browse all episodes without downloading anything:

```bash
cowado check https://comic-walker.com/detail/KC_003002_S
```

```
  青春ヒストリカ
  ────────────────

  ✓  [12] 第12話  ← CURRENT
  ✓  [11] 第11話
  ✗  [10] 第10話  (locked)
  ...

  12 episode(s) total · 10 available
```

---

#### `cowado version`

```bash
cowado version
```
