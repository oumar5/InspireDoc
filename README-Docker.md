# 🐳 InspireDoc - Guide Docker

Ce guide explique comment utiliser InspireDoc avec Docker pour le développement et la production.

## 🚀 Démarrage rapide

### Prérequis

- Docker et Docker Compose installés
- Fichier `.env` configuré avec vos clés API

### Développement avec hot reload

```bash
# Méthode 1: Script automatisé (recommandé)
./docker-dev.sh start

# Méthode 2: Docker Compose manuel
docker-compose -f docker-compose.dev.yml up --build
```

L'application sera accessible sur `http://localhost:8501` avec hot reload activé.

## 📁 Structure Docker

### Fichiers Docker

- `Dockerfile` - Image multi-stage (développement + production)
- `docker-compose.yml` - Configuration de production
- `docker-compose.dev.yml` - Configuration de développement avec hot reload
- `.dockerignore` - Fichiers exclus du build
- `docker-dev.sh` - Script de développement automatisé

### Volumes et hot reload

En mode développement, le code source est monté comme volume :

```yaml
volumes:
  - .:/app                    # Code source (hot reload)
  - ./data:/app/data         # Données persistantes
  - /app/__pycache__         # Exclusion du cache Python
```

## 🛠️ Commandes de développement

### Script automatisé (`docker-dev.sh`)

```bash
# Démarrer en mode développement
./docker-dev.sh start

# Construire l'image
./docker-dev.sh build

# Arrêter les services
./docker-dev.sh stop

# Redémarrer
./docker-dev.sh restart

# Voir les logs
./docker-dev.sh logs

# Ouvrir un shell dans le conteneur
./docker-dev.sh shell

# Exécuter une commande
./docker-dev.sh exec pip install nouvelle-dependance

# Nettoyer les ressources
./docker-dev.sh clean
```

### Docker Compose manuel

```bash
# Développement
docker-compose -f docker-compose.dev.yml up --build
docker-compose -f docker-compose.dev.yml down

# Production
docker-compose up --build
docker-compose down
```

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` :

```env
# Configuration GPT-4o (OBLIGATOIRE)
GPT4O_API_KEY=votre_cle_api
GPT4O_ENDPOINT=https://votre-endpoint.openai.azure.com

# Configuration optionnelle
INSPIREDOC_DEBUG=true
INSPIREDOC_LOG_LEVEL=DEBUG
```

### Ports exposés

- `8501` - Interface Streamlit
- `6379` - Redis (développement uniquement)

## 🏗️ Architecture multi-stage

Le Dockerfile utilise une approche multi-stage :

### Stage `base`
- Image Python 3.11 slim
- Dépendances système (WeasyPrint, etc.)
- Dépendances Python communes

### Stage `development`
- Hérite de `base`
- Outils de développement (pytest, black, etc.)
- Configuration pour hot reload
- Variables d'environnement de debug

### Stage `production`
- Hérite de `base`
- Code application copié
- Configuration optimisée
- Healthcheck activé

## 🔄 Hot Reload

Le hot reload est activé via :

1. **Volume mounting** : Code source monté en temps réel
2. **Streamlit configuration** :
   ```env
   STREAMLIT_SERVER_FILE_WATCHER_TYPE=poll
   STREAMLIT_SERVER_RUN_ON_SAVE=true
   ```
3. **Python configuration** :
   ```env
   PYTHONDONTWRITEBYTECODE=1
   PYTHONUNBUFFERED=1
   ```

### Fichiers surveillés

- Tous les fichiers `.py`
- Fichiers de configuration
- Templates et assets

### Exclusions

- Cache Python (`__pycache__`)
- Fichiers temporaires
- Logs et données

## 📊 Monitoring et debugging

### Logs

```bash
# Suivre les logs en temps réel
docker-compose -f docker-compose.dev.yml logs -f

# Logs d'un service spécifique
docker-compose -f docker-compose.dev.yml logs -f inspiredoc-dev
```

### Debugging

```bash
# Accéder au conteneur
docker-compose -f docker-compose.dev.yml exec inspiredoc-dev bash

# Vérifier les processus
docker-compose -f docker-compose.dev.yml exec inspiredoc-dev ps aux

# Vérifier les variables d'environnement
docker-compose -f docker-compose.dev.yml exec inspiredoc-dev env
```

### Healthcheck

En production, un healthcheck vérifie que l'application répond :

```bash
# Vérifier le statut
docker-compose ps

# Tester manuellement
curl -f http://localhost:8501/healthz
```

## 🚀 Déploiement en production

### Build de production

```bash
# Construire l'image de production
docker build --target production -t inspiredoc:latest .

# Ou avec docker-compose
docker-compose build
```

### Démarrage en production

```bash
# Avec docker-compose
docker-compose up -d

# Avec Docker run
docker run -d \
  --name inspiredoc \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  inspiredoc:latest
```

## 🔧 Dépannage

### Problèmes courants

**Port déjà utilisé :**
```bash
# Vérifier les ports utilisés
lsof -i :8501

# Changer le port
docker-compose -f docker-compose.dev.yml up -p 8502:8501
```

**Problème de permissions :**
```bash
# Vérifier les permissions des volumes
ls -la data/

# Corriger si nécessaire
sudo chown -R $USER:$USER data/
```

**Cache Docker :**
```bash
# Rebuild sans cache
docker-compose build --no-cache

# Nettoyer le système Docker
docker system prune -a
```

**Hot reload ne fonctionne pas :**
```bash
# Vérifier le montage des volumes
docker-compose -f docker-compose.dev.yml exec inspiredoc-dev ls -la /app

# Redémarrer avec rebuild
./docker-dev.sh restart
```

## 📝 Bonnes pratiques

### Développement

1. **Utilisez le script `docker-dev.sh`** pour une expérience simplifiée
2. **Montez uniquement le code source** en développement
3. **Excluez les caches** Python du montage
4. **Utilisez des volumes nommés** pour les données persistantes

### Production

1. **Utilisez l'image de production** optimisée
2. **Configurez les healthchecks** appropriés
3. **Utilisez des secrets** pour les variables sensibles
4. **Montez les données** sur des volumes persistants

### Sécurité

1. **Ne commitez jamais** le fichier `.env`
2. **Utilisez des images** officielles et à jour
3. **Limitez les privilèges** des conteneurs
4. **Scannez les vulnérabilités** régulièrement

---

**Développement rapide avec Docker + Hot Reload = 🚀 Productivité maximale !**