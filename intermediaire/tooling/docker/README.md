# Docker

Docker est une plateforme de virtualisation qui permet de déployer des applications de manière isolée, et de manière reproductible. Elle se base sur le concept de conteneur, qui est une abstraction logicielle qui regroupe l'application, ses dépendances, et ses configurations, afin de garantir un comportement homogène entre différents environnements.

## Composantes de docker

Pour assurer un fonctionnement reproductible, docker se base sur plusieurs notions :

1. L'image docker va spécifier, dans un langage de programmation normé, les dépendances & les configurations de l'application. Un exemple d'application python minimal se définit dans le Dockerfile suivant :

```Dockerfile
# Utilisation de l'image officielle de python 3.10
FROM python:3.10

# Copie du code source dans le conteneur
COPY . /app

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances
RUN pip install -r requirements.txt

# Commande par défaut à lancer lors du démarrage du conteneur
CMD ["python", "app.py"]
```

2. Le conteneur docker est une instance d'une image docker. En se déployant sur une machine hôte, dont il va partager le noyau du système d'exploitation, le conteneur va pouvoir utiliser les ressources de la machine hôte, tout en isolant l'application de l'environnement, via les namespaces & cgroups Linux.

Pour passer du Dockerfile à un conteneur, il faut que l'image soit construite, ce qui se fait via la commande `docker build` :

```bash
docker build -t nom_de_l_image:tag -f Dockerfile .
```

3. Les volumes docker permettent de persister les données de l'application, en les stockant sur le disque dur de la machine hôte. Cela permet également de partager des fichiers depuis la machine hôte vers le conteneur, comme par exemple des clés ssh ou autres secrets, partagés au runtime mais non définis dans l'image docker.

4. Docker permet également de déployer des réseaux virtuels, entre les conteneurs, avec la machine hôte, ou vers d'autres hôtes. Pour cela, le docker engine permet de définir 3 types de réseaux :

- `bridge` : un réseau virtuel entre les conteneurs, permettant de les rendre accessibles entre eux.
- `host` : un réseau virtuel entre le conteneur & la machine hôte, permettant de les rendre accessibles entre eux.
- `overlay` : un réseau virtuel entre les conteneurs, ou entre le conteneur & un autre hôte, permettant de les rendre accessibles entre eux. Ce type de réseau est utilisé notamment par les orchestrateurs Swarm & Kubernetes.


### Installation

La procédure d'installation la plus simple, pour les 3 plateformes les plus répandues, est de le faire via docker desktop, qui embarque le docker engine, docker compose, et une interface graphique permettant de gérer les conteneurs, images, volumes, réseaux, etc.

- [Linux](https://docs.docker.com/desktop/install/linux-install/)
- [Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Windows](https://docs.docker.com/desktop/install/windows-install/)

Pour [Linux](https://docs.docker.com/engine/install/#supported-platforms), il est également possible de le faire via apt, avec comme première étape l'ajout des repositories officiels (exemple pour ubuntu 24) :

```bash
# Ajout de la clé GPG officielle de Docker
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Ajout du repository officiel de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Ensuite, l'installation des différents composants :

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### BuildX

Installé manuellement via la commande apt précédente, BuildX est une extension de docker, qui permet de construire des images docker multi-plateformes, c'est à dire qui peuvent être déployées sur différentes architectures (x86, arm, etc). Cela peut être nécessaire pour gérer la distribution des images docker entre des plateformes différentes entre le développement & le production, par exemple.
BuildX peut s'utiliser dans une commande de build classique :

```bash
docker build -t image_name:tag --platform linux/amd64 -f Dockerfile .
```
