<!-- i18readme -->
[English](../README.md) | [Русский](README.ru.md) | **中文**
<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.11%20%7C%203.12%20%7C%203.13%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

从 [ComicWalker](https://comic-walker.com) 下载漫画图片的命令行工具。

> ⚠️ 请勿使用本工具侵犯任何著作权。

---

### 安装

需要 **Python 3.11+**，可从 [python.org](https://www.python.org/downloads/) 下载。

```bash
pip install cowado
```

---

### 快速开始

粘贴任意 ComicWalker 链接，然后选择一话：

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

整个流程就是这样：选择一话，选择图片尺寸，然后等待。

任何 ComicWalker 链接都可以使用 —— 作品页面或直接的单话链接，带不带查询参数都行：

```bash
cowado https://comic-walker.com/detail/KC_000097_S
cowado https://comic-walker.com/detail/KC_000097_S?episodeType=first
cowado https://comic-walker.com/detail/KC_000097_S/episodes/KC_0000970000100011_E
```

---

### 如何阅读话数列表

```
    #1  (13 pages)  第1話
 #4-15  locked
   #16    (1 page)  1巻発売記念イラスト
```

- **`#1`** 是话数编号。用 `--episode=1` 传入即可跳过选择菜单，直接下载该话。
- **`#4-15  locked`** 表示第 4 至 15 话目前不免费。它们会显示出来让你知道有哪些内容，但无法选中。
- 有些条目根本不是正篇 —— 而是插图或公告。看页数就能分辨。

---

### 命令

#### `cowado <url>`

`cowado download <url>` 的简写，两者作用相同。

#### `cowado check <url>`

只显示话数列表，不下载任何内容。

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

### 参数

| 参数                    | 作用                                                        |
| ----------------------- | ----------------------------------------------------------- |
| `--episode=N`           | 直接下载第 N 话，不再询问                                    |
| `--size=max`            | 直接指定图片尺寸：`max`、`min`、`mobile`、`desktop`          |
| `--output_dir="./path"` | 保存到其他位置（默认为 `{漫画标题}/{话数编号}/`）            |

```bash
# 全程无需回答任何问题
cowado <url> --episode=5 --size=max --output_dir="./manga"
```

**关于 `--size`。** ComicWalker 提供两种图片尺寸，哪一种更大取决于具体作品。`max` 和 `min` 始终按实际尺寸选择，因此在脚本中使用最为可靠。`mobile` 的宽度固定为 768 像素；`desktop` 受高度限制，根据作品不同，宽度可能在 650 到 1284 像素之间。

---

### 文件保存位置

```
逢魔暮らしの奴さん/
└── 003/
    ├── 001.webp
    ├── 002.webp
    └── ...
```

每话一个文件夹，页面按编号命名。可用 `--output_dir` 更改保存位置。

---

### 出现问题时

设置 `COWADO_DEBUG=1` 可以看到完整的错误信息，而不只是一行提示。

```bash
COWADO_DEBUG=1 cowado <url>
```

## Star History

[![Star History Chart](https://api.star-history.com/image?repos=Timolio/ComicWalkerDownloader&type=date&legend=top-left)](https://www.star-history.com/?repos=Timolio%2FComicWalkerDownloader&type=date&legend=top-left)
