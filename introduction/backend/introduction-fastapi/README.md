# Introduction à FastAPI

## Qu'est-ce que FastAPI ?

FastAPI est un framework web moderne pour construire des APIs avec Python. Il se distingue par :

- **Performance** : Gestion de la concurence & des requêtes asynchrones, contrairement à Flask.
- **Intuitif** : Supporté par VSCode et PyCharm, encourage l'apprentissage des concepts fondamentaux via une API claire et ouverte.
- **Simple & concis** : Conçu pour être facile à utiliser et à apprendre, minimise la duplication de code
- **Robuste** : Code orienté production avec des features intégrées de manière standard : documentation, validation de données, gestion des erreurs...

## Exemple Minimal

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello DataForGood!"}
```

## Installation

```bash
# Python 3.7+
python --version

# Installation
pip install fastapi[all]
pip install uvicorn
```

## Ressources

- [Documentation Officielle FastAPI](https://fastapi.tiangolo.com/)
- [Tutoriel Interactif](./exemples/tutorial/)
