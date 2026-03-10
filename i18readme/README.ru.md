<!-- i18readme -->
[English](../README.md) | **Русский** | [Deutsch](README.de.md) | [Français](README.fr.md) | [中文](README.zh.md)
<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

CLI-инструмент для скачивания манги с [ComicWalker](https://comic-walker.com).

> ⚠️ Убедитесь, что вы не используете этот инструмент для нарушения авторских прав.

---

### Установка

Требуется **Python 3.8+**. Скачать можно с [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

---

### Использование

#### `cowado download <url>`

Передайте любую ссылку с ComicWalker — страницу серии, прямую ссылку на эпизод или ссылку с query-параметрами:

```bash
cowado download https://comic-walker.com/detail/KC_008483_S
cowado download https://comic-walker.com/detail/KC_008483_S?episodeType=first
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E?episodeType=latest
...
```

Инструмент загружает информацию о манге и показывает, что нашёл:

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

Страницы сохраняются в формате `.webp` с именами по номеру страницы (`001.webp`, `002.webp`, ...).

---

#### Флаги

| Флаг                    | Описание                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `--episode=N`           | Пропустить выбор и сразу скачать эпизод N                                             |
| `--output_dir="./path"` | Переопределить директорию сохранения (по умолчанию: `{название манги}/{номер эпизода}/`) |

```bash
# Скачать эпизод 5 напрямую в указанную папку
cowado download <url> --episode=5 --output_dir="./manga"
```

---

#### `cowado check <url>`

Просмотр всех эпизодов без скачивания:

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

## История звёзд

[![Star History Chart](https://api.star-history.com/image?repos=Timolio/ComicWalkerDownloader&type=date&legend=top-left)](https://www.star-history.com/?repos=Timolio%2FComicWalkerDownloader&type=date&legend=top-left)