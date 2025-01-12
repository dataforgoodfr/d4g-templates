# Exposer une base de données via FastAPI

## Mapping applicatif & base de données

Ce tutoriel montre comment exposer une base de données en REST, pour exécuter des opérations de type CRUD.
La connexion à la base de données sera gérée par sqlalchemy, la couche HTTP via FastAPI. Le setup initial comprend la mise en place d'une base postgres, via [docker compose](../../intermediaire/tooling/docker/Docker_compose.md) par exemple
L'ORM sqlalchemy est disponible via pip:

```bash
uv pip install sqlalchemy
```

Fait pour faire interagir les objets créés dans le domaine applicatif avec ceux persistés dans la base de données, cette librairie va permettre de générer le code SQL nécessaire aux opérations faites par l'application, en définissant une syntaxe de synchronisation entre les objets et la base de données.

En premier lieu, les tables permettant le mapping entre les objets et la base de données doivent être créées : 

```python

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
```

Ici, les attributs de la classe & leurs métadonnées définissent les colonnes, les types ainsi que les relations entre les tables.

Nous pouvons ensuite définir la session qui nous permettra de nous connecter à la base de données, et d'exécuter les requêtes SQL nécessaires :

```python
from sqlalchemy import create_engine, sessionmaker
DB_URL = "postgresql://user:password@localhost:5432/database"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Puis utiliser cette session pour exécuter les opérations CRUD : 

# Créer un produit
product = Product(name="Product 1", price=10.0)
session.add(product)
session.commit()

# Lire un produit
product = session.query(Product).filter(Product.id == 1).first()
print(product.name)

# Mettre à jour un produit
product.price = 15.0
session.update(product)
session.commit()

# Supprimer un produit
session.delete(product)
session.commit()
```

Un commit est nécessaire pour valider les opérations d'écriture sur la base de données.

Une fois définies, ces opérations peuvent être utilisées dans une application FastAPI, pour les exposer en HTTP : 

```python
def get_products(): 
    products = session.query(Product).all()
    return products

@app.get("/products")
def get_products():
    return get_products()
```

## Architecture applicative

Si cette simplicité de mise en place permet de rapidement exposer une table via HTTP, cette implémentation va rapidement montrer quelques limites :

- Difficulté de réutiliser les fonctions d'accès / écriture, qui doivent partager une session.
- En cas de nombre important d'appels, le nombre de sessions connectées à la base de données va être limité par le nombre de connexions autorisées par le serveur de base de données.
- Au fur et à mesure du développement applicatif, les contraintes métiers de validation de données vont émerger, rendant ces méthodes de manipulation de la base de données potentiellement très complexes.

Afin de limiter ces problèmes, l'architecture de l'application doit être pensée pour favoriser l'évolution (notamment des règles métiers) et des contraintes techniques. Pour cela, la clean architecture propose quelques patrons de conception, permettant de séparer les responsabilités de l'application.

Mise en place sur une application FastAPI, cela donne une arborescence de fichiers de type :

```bash
.
├── app
│   ├── api
│   │   ├── product.py
│   ├── domain
│   ├── infra
│   │   ├── repositories
│   │   │   ├── models.py
│   │   │   └── product.py
│   ├── usecases
│   │   └── product.py
│   └── schemas.py
```

L'avantage de ce découpage est de séparer les définitions techniques des données, utiles notamment pour les accès à la base de données, des notions plus orientées métier, qui porteront la logique la plus importante.
Ce découplage permet faire évoluer les deux types de représentation de la donnée indépendamment, en favorisant l'évolution de la logique métier, les éléments techniques (définis dans le dossier infrastructure) ne devant qu'être des supports à la logique métier.

Pour notre exemple, nous retrouverons donc l'opération get_products dans 3 couches distinces :

- la couche domain, qui définira les objets métiers ainsi que la représentation de la couche HTTP :

```python
class Product:
    id: int
    name: str
    price: float
```

- la couche repository, qui définira les accès & élements de persistence dans la base de données :

```python
class ProductRepository:
    def get_products(self):
        db_products = session.query(Product).all()
        return [self.map_to_domain(product) for product in db_products]
    
    def map_to_domain(self, product):
        return Product(id=product.id, name=product.name, price=product.price)
```

En général, il est utile de définir des méthodes de mapping entre les éléments techniques de la base de données et les objets métiers, permettant de séparer les responsabilités de la couche repository, qui ne doit pas être chargée de la logique métier, et inversement. Ces mappers seront simples à faire évoluer dans le futur et permettent d'éviter de polluer un modèle métier avec des attributs techniques.

- la couche usecase, qui définira la mise en oeuvre de la logique métier sur les éléments techniques de l'infrastructure :

```python
class ProductUsecase:
    def get_products(self):
        return ProductRepository().get_products()
```

Cette couche pourra évoluer dans le futur, pour ajouter des nuances métiers, comme par exemple un filtre sur le prix des produits, sans pour autant modifier les couches techniques, qui pourront être réutilisées par d'autres cas d'usages métiers.

Pour finir, nous pouvons exposer ce cas d'usage métier via une route FastAPI :

```python
@app.get("/products")
def get_products():
    return ProductUsecase().get_products()
```


## Références

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Cosmic Python](https://cosmicpython.com/)