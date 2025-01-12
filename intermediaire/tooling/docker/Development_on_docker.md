# Fabriquer un environnement de développement avec Docker, étape par étape

Ce tutoriel, traduit & adapté de l'article suivant : [Building a development environment with Docker, step by step](https://www.freecodecamp.org/news/building-a-development-environment-with-docker-step-by-step/), propose de lister toutes les étapes nécessaires pour créer un environnement de développement fonctionnel sous Docker.

## Prérequis

1. Installer Docker

En version desktop, depuis la documentation officielle : [Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [Mac](https://docs.docker.com/desktop/setup/install/mac-install/) ou [Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/).

En version engine seule, pour [Linux](https://docs.docker.com/engine/install/)

## Getting started

La première étape est de récupérer une image depuis le répertoire public de Docker, Docker Hub.
Pour ça, il faut en premier lieu s'authentifier :

```bash
docker login docker.io
Authenticating with existing credentials...
Login Succeeded
```

Une fois authentifié, il est possible de récupérer (`pull`) une image qui contient python en version 3.10:

```bash
docker pull python:3.10
```

Si c'est la première fois, docker va télécharger chacune des couches de l'image, par la suite, il ne le fera que si une des couches est manquante ou doit être mise à jour.

```bash
3.10: Pulling from library/python
66932e2b787d: Pull complete
4afa7e263db1: Pull complete
c812910e5e62: Pull complete
f4e4299bb649: Pull complete
5213cc2f9120: Pull complete
4a3b5b2f0e66: Pull complete
c214ceb1cabf: Pull complete
f5336038b15c: Pull complete
Digest: sha256:f94601bb6374b0b63835a70c9e5c3ba1b19bc009133900a9473229a406018e46
Status: Downloaded newer image for python:3.10
docker.io/library/python:3.10
````

Pour voir quelles images sont disponibles localement, il est possible d'utiliser la commande `docker images`:

```bash
docker images
REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
python       3.10      f7537c504c9a   7 days ago   1.01GB
```

L'image est bien présente, il est maintenant possible de l'utiliser!
Pour ça, il faut lancer un container basé sur cette image, avec 2 options particulières : `--interactive` & `--tty`, ou `-it`. Elles permettront de se connecter au container avec un terminal :

```bash
docker run -it python:3.10
```

Depuis ce terminal, on a donc maintenant la possibilité de jouer des scripts python ou de lancer un interpréteur:

```bash
docker run -it python:3.10      
Python 3.10.15 (main, Nov 13 2024, 15:54:19) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

La version de python est fonctionnelle, il est temps maintenant d'ajouter les dépendances nécessaires au projet, de manière reproductible, pour pouvoir partager cet environnement avec d'autres développeurs.
Pour fixer cette procédure d'installation, Docker fournit un outil de personalisation de l'image de base, le `Dockerfile`. Créons donc un exemple, qui aura les fonctionnalités suivantes :

- Importe l'image de base, avec python en version 3.10
- Installer le gestionnaire de paquets `uv`
- Mettre en place un environnement virtuel
- Installer les dépendances nécessaires au projet
- Installer un editeur de code, vim
- Définir la commande de démarrage du container, un terminal bash

### Personaliser l'image de base avec un Dockerfile

#### Environnement virtuel

Pour créer un environment virtuel, nous allons avoir besoin de récupérer le gestionnaire de paquets `uv` et de l'installer. Pour cela, la [documentation officielle](https://docs.astral.sh/uv/guides/integration/docker/#installing-uv) nous propose de récupérer le script d'installation et de l'exécuter.

```dockerfile
FROM python:3.10

# Ajoutons curl et les certificats nécessaires pour télécharger l'archive de la release
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Téléchargeons le script d'installation
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Exécutons le script d'installation puis supprimons le
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Assurons que le binaire installé est sur le PATH
ENV PATH="/root/.local/bin/:$PATH"
```

#### Spécifier les dépendances

2 options sont possibles :

- Créer un fichier `requirements.txt`, qui listera toutes les dépendances et leurs versions :

```txt
pandas==2.2.1
matplotlib==3.8.3
```

- Créer un fichier `pyproject.toml`, qui définira un peu plus précisement le projet, ses dépendances, et les outils associés :

```toml
[project]
name = "nom-du projet"
version = "0.1.0"
description = "Description du projet"
requires-python = "3.10"
dependencies = [
    "pandas>=2.2.1,<3.0.0",
    "matplotlib>=3.8.3,<4.0.0",
]
```

Une fois ces fichiers en place, il est possible de les utiliser pour installer les dépendances du projet, dans l'environnement virtuel créé :

```bash
uv venv
uv pip sync requirements.txt

```

ou, dans le cadre du fichier `pyproject.toml` :

```bash
uv venv
uv sync
```

#### Editeur de code

A l'intérieur du container, il est parfois utile de pouvoir éditer de la configuration, ou directement des fichiers de code. Pour ça, il est possible d'installer un éditeur de code, comme `vim`.

```dockerfile
RUN apt-get update && apt-get install -y vim
```

D'autres utilitaires courants peuvent être installés, comme `curl` pour les requêtes HTTP, `build-essential` pour compiler du code C, `ca-certificates` pour les certificats SSL, `libpq-dev` pour les dépendances de la librairie `psycopg2`, utile pour les bases de données PostgreSQL, etc.

Une fois cette mise en place terminée, il est temps de compiler ces étapes dans un Dockerfile, et d'ajouter la commande de démarrage du container, le terminal bash :

```dockerfile
FROM python:3.10

# Ajoutons curl et les certificats nécessaires pour télécharger l'archive de la release
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Téléchargeons le script d'installation
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Exécutons le script d'installation puis supprimons le
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Assurons que le binaire installé est sur le PATH
ENV PATH="/root/.local/bin/:$PATH"


# Ajoutons le fichier pyproject.toml dans le répertoire de travail
ADD pyproject.toml /dev/pyproject.toml

# Définissions l'environnement virtuel de travail
WORKDIR /dev
RUN uv venv
RUN uv sync

# Puis, automatiquement activer l'environnement virtuel au lancement du terminal
RUN echo "source /dev/.venv/bin/activate" >> ~/.bashrc

# Installer vim
RUN apt-get update && apt-get install -y vim

# Définir la commande de démarrage du container, le terminal bash   
CMD ["bash"]
```

Et voilà, l'image est maintenant prête à être utilisée! Pour l'utiliser, il suffit de la build, puis de la lancer avec les commandes suivantes :

```bash
docker build -t python-dev -f Dockerfile .
docker run -it --rm python-dev
```