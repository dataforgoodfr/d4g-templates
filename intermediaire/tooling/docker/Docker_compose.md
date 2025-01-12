# Docker compose

Pour faire collaborer plusieurs services ou applications déployés via docker localement, docker compose propose une abstraction simple et extensible. En gérant un outillage réseau, les variables d'environnement & la dépendance entre services notamment, docker compose permet de déployer des applications complexes avec un minimum de configuration, et de manière reproductible.

## Installation

Docker compose est embarqué avec docker desktop, qui reste la manière la plus simple d'installer docker & le docker engine, sur les 3 plateformes les plus répandues :

- [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- [Mac](https://docs.docker.com/desktop/setup/install/mac/)
- [Windows](https://docs.docker.com/desktop/setup/install/windows/)


Sur linux, il est également possible de l'installer sous forme de plugin, après avoir installé le docker engine.

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

Afin de vérifier que docker compose est bien installé, il est possible de lancer la commande suivante :

```bash
docker compose version
```

## Lier un ensemble de services

Docker compose fonctionne avec un fichier `docker-compose.yml` qui va spécifier l'ensemble des composants à déployer. Par exemple, le compose suivant va lier 2 applications, qui communiquent entre elles via un réseau bridge :

```yaml
services:
  backend:
    # Image docker à utiliser, qui sera ici lue depuis le registre local d'images, ou depuis le docker hub si l'image n'est pas présente localement.
    image: backend:latest
    # Ports à exposer, ici le backend est exposé sur le port 8080.
    ports:
      - "8081:8081"
    # Variables d'environnement à passer au conteneur.
    environment:
      LOG_LEVEL: DEBUG
      DATABASE_URL: localhost:5432
    # Réseau à utiliser, ici le réseau bridge par défaut.
    networks:
      - default
  frontend:
    # Il est possible de spécifier un Dockerfile à utiliser pour construire l'image, ici depuis le répertoire courant.
    build:
      context: .
      dockerfile: docker/frontend.Dockerfile
    ports:
      - "8080:8080"
    networks:
      - default

# Définition du réseau bridge par défaut, qui permet de faire communiquer les services entre eux.
networks:
  default:
    driver: bridge
```

Pour lancer le compose, il suffit de lancer la commande suivante :

```bash
docker compose up
```

Ou spécifier quel service lancer, depuis un fichier spécifique `docker-compose.yml` :

```bash
docker compose up backend -f docker-compose.yml
```

L'ajout de l'option `-d` permet de démarrer le service en arrière plan, c'est à dire en mode daemon.

Pour stopper le service, il suffit de lancer la commande suivante :

```bash
docker compose down
```

En plus d'applications locales, il est possible de déployer des services externes, comme des bases de données par exemple :

```yaml
  postgres:
    environment:
      HOSTNAME: ${DATABASE_HOST:-postgres}
      POSTGRES_DB: ${DATABASE_NAME:-app_db}
      POSTGRES_PASSWORD: ${DATABASE_PASS:-supersecret}
      POSTGRES_USER: ${DATABASE_USER:-app-user}
    # Cette image officielle de postgres est lue sur le docker hub.
    image: postgres:13
    ports:
      - 5480:5432
    restart: unless-stopped
    # On monte un volume pour persister les données de la base de données, et pouvoir récupérer les données après un redémarrage.
    volumes:
      - postgres_data:/var/lib/postgresql/data:rw
    networks:
      - default

  pgadmin:
    # Cette image officielle de pgadmin est lue sur le docker hub.
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL:-test@test.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD:-test}
    volumes:
      - pgadmin:/root/.pgadmin
      - ./config/pgpassfile:/pgadmin4/pgpassfile
      - ./config/pgadmin-servers.json:/pgadmin4/servers.json
    ports:
      - "${PGADMIN_PORT:-5080}:80"
    networks:
      - default
    restart: unless-stopped
```

Pour une application plus complexe, regarder l'exemple du fichier [bloom](./examples/docker_compose/bloom.yaml).
