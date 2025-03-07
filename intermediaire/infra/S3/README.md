#S3 (Simple Storage Service)

S3 est une norme de service de stockage d'objets inventé par AWS (Amazon Web Services) et maintenant proposé dans la plupart des cloud provider. Il permet de stocker, organiser et récupérer des données sous forme d'objets, avec une haute disponibilité, une durabilité exceptionnelle, et des fonctionnalités avancées comme la gestion des accès, le versioning, et le chiffrement.

## Principes de fonctionnement

S3 repose sur des concepts simples mais puissants :

1. **Buckets** :  
   Les objets sont stockés dans des conteneurs appelés *buckets*. Chaque bucket est associé à un nom unique au sein de la région AWS dans laquelle il est créé. Les buckets peuvent être configurés pour répondre à différents besoins (accès public/privé, règles de versioning, etc.).

   Exemple de création d'un bucket avec AWS CLI :
   ```bash
   aws s3api create-bucket --bucket nom-du-bucket --region us-east-1
   ```

2. **Objets** :  
   Chaque objet dans S3 se compose de trois parties :
   - Les données (le fichier stocké, par exemple une image, un document, une vidéo, etc.).
   - Une clé (le nom unique de l'objet dans le bucket, par exemple `images/chat.jpg`).
   - Des métadonnées optionnelles (informations supplémentaires sur l'objet, comme son type MIME).

   Exemple d'envoi d'un fichier dans un bucket via AWS CLI :
   ```bash
   aws s3 cp chemin/vers/fichier.txt s3://nom-du-bucket/fichier.txt
   ```

3. **Classes de stockage** :  
   S3 propose plusieurs classes de stockage adaptées à différents cas d'usage :
   - **S3 Standard** : pour des accès fréquents, avec une faible latence.
   - **S3 Intelligent-Tiering** : ajuste automatiquement la classe de stockage en fonction des modèles d'accès.
   - **S3 Standard-IA (Infrequent Access)** : pour des données moins fréquemment consultées.
   - **S3 Glacier** et **Glacier Deep Archive** : pour l'archivage à long terme à faible coût.

   Exemple de modification de la classe de stockage :
   ```bash
   aws s3api copy-object \
     --bucket nom-du-bucket \
     --copy-source nom-du-bucket/fichier.txt \
     --key fichier.txt \
     --storage-class STANDARD_IA
   ```

4. **Gestion des permissions** :  
   L'accès aux buckets et aux objets est contrôlé via des politiques d'accès (IAM, ACL, et policies de bucket) :
   - **IAM Policies** : définissent les permissions des utilisateurs/roles AWS.
   - **Bucket Policies** : permettent de gérer les accès globaux au niveau du bucket.
   - **Access Control Lists (ACL)** : définissent des permissions spécifiques sur un objet ou un bucket.

   Exemple de politique de bucket pour un accès public en lecture :
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::nom-du-bucket/*"
       }
     ]
   }
   ```

5. **Versioning** :  
   Le versioning permet de conserver plusieurs versions d'un objet dans un bucket, pour éviter les pertes de données ou restaurer une version antérieure.

   Activation du versioning :
   ```bash
   aws s3api put-bucket-versioning --bucket nom-du-bucket --versioning-configuration Status=Enabled
   ```

6. **Chiffrement** :  
   S3 prend en charge le chiffrement des données au repos, à l'aide de clés AWS gérées (SSE-S3), de clés clients (SSE-C), ou de clés KMS (SSE-KMS).

   Exemple d'activation du chiffrement par défaut dans un bucket :
   ```bash
   aws s3api put-bucket-encryption --bucket nom-du-bucket --server-side-encryption-configuration \
     '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
   ```

---

## Installation et configuration de l'AWS CLI

Pour utiliser un S3 au sein de votre application, vous pouvez utiliser une librairie Python comme Boto3. Des examples sont fournis dans le dossier examples/ . Pour interagir avec S3 depuis votre machine sans développer, l'AWS CLI est par contre l'outil le plus simple. Voici les étapes d'installation et de configuration :

1. **Installation de l'AWS CLI** :
   - [Linux](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#install-linux)
   - [Mac](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#install-macos)
   - [Windows](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#install-windows)

   Exemple pour une installation rapide sur Linux :
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **Configuration de l'AWS CLI** :
   Une fois installé, configurez l'outil avec vos identifiants AWS :
   ```bash
   aws configure
   ```
   Vous devrez fournir vos clés d'accès AWS, votre région par défaut (ex. `us-east-1`), et le format de sortie préféré (`json`, `text` ou `table`).

---

## Commandes S3 courantes

### Upload de fichiers
Envoyer un fichier sur S3 :
```bash
aws s3 cp chemin/vers/fichier.txt s3://nom-du-bucket/
```

### Téléchargement de fichiers
Télécharger un fichier depuis S3 :
```bash
aws s3 cp s3://nom-du-bucket/fichier.txt chemin/local/
```

### Synchronisation
Synchroniser un dossier local avec un bucket S3 :
```bash
aws s3 sync chemin/local/ s3://nom-du-bucket/
```

### Liste des objets
Lister tous les objets dans un bucket :
```bash
aws s3 ls s3://nom-du-bucket/
```

### Suppression d'objets
Supprimer un objet dans un bucket :
```bash
aws s3 rm s3://nom-du-bucket/fichier.txt
```

---

## Fonctionnalités avancées

### Accès statique
Les buckets S3 peuvent être configurés pour héberger des sites web statiques. Cela inclut des fichiers HTML, CSS, JavaScript, ou même des images.

Configuration d'un bucket pour l'hébergement statique :
```bash
aws s3 website s3://nom-du-bucket/ --index-document index.html --error-document error.html
```

### Intégration avec d'autres services AWS
S3 s'intègre avec plusieurs services AWS, comme :
- **CloudFront** : pour la distribution de contenu.
- **Athena** : pour analyser des fichiers S3 avec SQL.
- **Lambda** : pour déclencher des traitements lors d'événements S3 (exemple : upload d'un fichier).

---

Pour plus d'informations, visitez la [documentation officielle d'AWS S3](https://docs.aws.amazon.com/s3/).
```
