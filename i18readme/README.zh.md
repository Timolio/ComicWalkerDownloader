<!-- i18readme -->

[English](../README.md) | [Русский](README.ru.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | **中文** | [日本語](README.ja.md)

<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

用于从 [ComicWalker](https://comic-walker.com) 下载漫画图片的命令行工具。

> ⚠️ 请勿将本工具用于任何侵犯版权的行为。

---

### 安装

需要 **Python 3.8+**，请从 [python.org](https://www.python.org/downloads/) 下载。

```bash
pip install cowado
```

---

### 使用方法

#### `cowado download <url>`

传入任意 ComicWalker 链接 —— 可以是系列页面、单话直链，或者带查询参数的链接：

```bash
cowado download https://comic-walker.com/detail/KC_008483_S
cowado download https://comic-walker.com/detail/KC_008483_S?episodeType=first
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E?episodeType=latest
...
```

青春ヒストリカ
────────────────
12 episode(s) available

? Select episode to download:
❯ [12] 第12話 ← CURRENT
[11] 第11話
[10] 第10話
...

Downloading → [12] 第12話
Saving to → /home/user/青春ヒストリカ/012/

████████████████████████ 22/22 pages

✓ Done! /home/user/青春ヒストリカ/012/

````

每一页会保存为 `.webp` 文件，按页码命名（`001.webp`、`002.webp`……）。

---

#### 参数选项

| 参数                    | 说明                                             |
| ----------------------- | ------------------------------------------------ |
| `--episode=N`           | 跳过选择，直接下载第 N 话                        |
| `--output_dir="./path"` | 自定义输出目录（默认：`{漫画标题}/{话数编号}/`） |

```bash
# 直接下载第 5 话到指定文件夹
cowado download <url> --episode=5 --output_dir="./manga"
````

---

#### `cowado check <url>`

浏览所有话数，不下载任何内容：

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
