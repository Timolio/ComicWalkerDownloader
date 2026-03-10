<!-- i18readme -->
[English](../README.md) | [Русский](README.ru.md) | [Deutsch](README.de.md) | **Français** | [中文](README.zh.md) | [日本語](README.ja.md)
<!-- i18readme -->

<br>

[![PyPI - Version](https://img.shields.io/pypi/v/cowado?color=blue)](https://pypi.org/project/cowado/)
[![Static Badge](https://img.shields.io/badge/python-%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20-blue)](https://www.python.org/downloads/)
[![PyPI Downloads](https://static.pepy.tech/badge/cowado)](https://pepy.tech/projects/cowado)

## ComicWalkerDownloader aka cowado

<img width="619" height="331" alt="Image" src="https://github.com/user-attachments/assets/e8aa40c5-e9c3-47f6-b29f-b5babb5c7cfb" />

Outil en ligne de commande pour télécharger des images de manga depuis [ComicWalker](https://comic-walker.com).

> ⚠️ Assurez-vous de ne pas utiliser cet outil en violation des lois sur le droit d'auteur.

---

### Installation

**Python 3.8+** est requis. Téléchargez-le depuis [python.org](https://www.python.org/downloads/).

```bash
pip install cowado
```

---

### Utilisation

#### `cowado download <url>`

Passez n'importe quelle URL ComicWalker — une page de série, un lien direct vers un épisode, ou une URL avec des paramètres :

```bash
cowado download https://comic-walker.com/detail/KC_008483_S
cowado download https://comic-walker.com/detail/KC_008483_S?episodeType=first
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E
cowado download https://comic-walker.com/detail/KC_008483_S/episodes/KC_0084830000200011_E?episodeType=latest
...
```

L'outil récupère les informations du manga et affiche ce qu'il a trouvé :

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

Les pages sont enregistrées en fichiers `.webp`, nommées par numéro de page (`001.webp`, `002.webp`, ...).

---

#### Options

| Option                  | Description                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| `--episode=N`           | Ignore la sélection et télécharge directement l'épisode N                                      |
| `--output_dir="./path"` | Remplace le répertoire de sortie (par défaut : `{titre du manga}/{numéro de l'épisode}/`) |

```bash
# Télécharger directement l'épisode 5 dans un dossier personnalisé
cowado download <url> --episode=5 --output_dir="./manga"
```

---

#### `cowado check <url>`

Parcourir tous les épisodes sans rien télécharger :

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