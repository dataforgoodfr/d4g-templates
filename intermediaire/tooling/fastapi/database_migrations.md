# Gestion des migrations de base de données

Lors du cycle de développement d'une application, le schéma et les données présentes dans la base de données vont régulièrement évoluer. Afin de pouvoir appliquer ces évolutions, pouvoir les rétrograder en cas d'incompatibilité ou de pouvoir les partager entre plusieurs développeurs et environnements, des outils de migrations permettent de faire ces évolutions de manière reproductible, comme [Alembic](https://alembic.sqlalchemy.org/).

Alembic s'install via pip :

```bash
uv pip install alembic
```

Et permet de génerer une configuration initiale, définissant les migrations à appliquer sur le projet, avec la structure suivante :

```bash
.
app/
├── alembic/
│   ├── alembic.ini # configuration de Alembic
│   ├── env.py # configuration de l'environnement
│   ├── script.py.mako # template de script de migration
│   └── versions/ # répertoire des migrations
│       ├── 1fd83d22bd1e_create_product_table.py # Migration initiale
│       ├── 234567890ab_add_product_description.py # Migration ajoutant une colonne description à la table product
│       └── 345678901cd_add_product_price.py # Migration ajoutant une colonne price à la table product
```

Pour ce faire, initialisons alembic :

```bash
alembic init alembic
```

Cette commande va créer l'arborescence ci dessus, et nous permettre de définir notre première migration : 

```bash
alembic revision -m "Create product table"
```

Ce qui nous donne un fichier de migration vide, à compléter comme ceci : 

```python
"""Create product table

Revision ID: 983f00ffb3a9
Revises: 
Create Date: 2025-01-12 11:40:33.752974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identifiants de la revision, utilisés par Alembic.
revision: str = '983f00ffb3a9'
# ici il n'y a pas de revision précédente, car c'est la migration initiale
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# La fonction upgrade applique les modifications pour créer les tables avec les attributs corrects
def upgrade() -> None:
    op.create_table('product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('price', sa.Float, nullable=False)
    )


# La fonction downgrade annule les modifications pour supprimer les tables
def downgrade() -> None:
        op.drop_table('product')
```

Cette migration peut ensuite être appliquée à la base de données avec la commande :

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
alembic upgrade head
```

Ce qui aura pour effet  d'appliquer la fonction d'upgrade, créer la table product & également créer une table alembic_version qui stocke l'état des migrations appliquées:
![alembic_version](alembic_version.png)
