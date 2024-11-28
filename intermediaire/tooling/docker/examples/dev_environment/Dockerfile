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
COPY ./pyproject.toml /app/pyproject.toml

# Définissions l'environnement virtuel de travail
WORKDIR /app
RUN uv venv
RUN uv sync

# Puis, automatiquement activer l'environnement virtuel au lancement du terminal
RUN echo "source /app/.venv/bin/activate" >> ~/.bashrc

# Installer vim
RUN apt-get update && apt-get install -y vim

# Définir la commande de démarrage du container, le terminal bash   
CMD ["bash"]