<!-- i18readme -->
[English](../README.md) | **Русский** | [中文](README.zh.md)
<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.11%20%7C%203.12%20%7C%203.13%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

Консольная утилита для скачивания страниц манги с [ComicWalker](https://comic-walker.com).

> ⚠️ Не используйте этот инструмент для нарушения авторских прав.

---

### Установка

Нужен **Python 3.11+**. Скачать можно на [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

---

### Быстрый старт

Вставьте любую ссылку с ComicWalker и выберите главу:

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

Весь процесс на этом и заканчивается: выбрать главу, выбрать размер картинок, подождать.

Подойдёт любая ссылка ComicWalker — страница тайтла или прямая ссылка на главу, с параметрами запроса или без:

```bash
cowado https://comic-walker.com/detail/KC_000097_S
cowado https://comic-walker.com/detail/KC_000097_S?episodeType=first
cowado https://comic-walker.com/detail/KC_000097_S/episodes/KC_0000970000100011_E
```

---

### Как читать список глав

```
    #1  (13 pages)  第1話
 #4-15  locked
   #16    (1 page)  1巻発売記念イラスト
```

- **`#1`** — номер главы. Передайте его как `--episode=1`, чтобы пропустить меню и сразу скачать эту главу.
- **`#4-15  locked`** — главы с 4 по 15 сейчас недоступны бесплатно. Они показаны, чтобы вы видели, что существует, но выбрать их нельзя.
- Некоторые записи вообще не главы — иллюстрации и анонсы. Их выдаёт число страниц.

---

### Команды

#### `cowado <url>`

Короткая форма `cowado download <url>`. Делают одно и то же.

#### `cowado check <url>`

Показать список глав, ничего не скачивая.

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

### Флаги

| Флаг                    | Что делает                                                              |
| ----------------------- | ----------------------------------------------------------------------- |
| `--episode=N`           | Скачать главу N без вопросов                                            |
| `--size=max`            | Выбрать размер без вопросов: `max`, `min`, `mobile`, `desktop`          |
| `--output_dir="./path"` | Сохранить в другое место (по умолчанию `{название манги}/{номер главы}/`) |

```bash
# ни одного вопроса
cowado <url> --episode=5 --size=max --output_dir="./manga"
```

**Про `--size`.** ComicWalker отдаёт два размера картинок, и какой из них крупнее — зависит от тайтла. `max` и `min` всегда выбирают по фактическому размеру, поэтому для скриптов надёжны именно они. `mobile` всегда даёт ширину 768 пикселей; `desktop` ограничен по высоте и в зависимости от тайтла оказывается где-то между 650 и 1284.

---

### Куда попадают файлы

```
逢魔暮らしの奴さん/
└── 003/
    ├── 001.webp
    ├── 002.webp
    └── ...
```

Одна папка на главу, страницы названы по номерам. Поменять место можно флагом `--output_dir`.

---

### Если что-то пошло не так

Переменная `COWADO_DEBUG=1` включает подробности ошибки вместо одной строки.

```bash
COWADO_DEBUG=1 cowado <url>
```

## Star History

[![Star History Chart](https://api.star-history.com/image?repos=Timolio/ComicWalkerDownloader&type=date&legend=top-left)](https://www.star-history.com/?repos=Timolio%2FComicWalkerDownloader&type=date&legend=top-left)
