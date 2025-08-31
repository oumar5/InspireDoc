# Dockerfile multi-stage pour InspireDoc

# Stage de base avec les dépendances système
FROM python:3.11-slim as base

# Installer les dépendances système essentielles
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    curl \
    fontconfig \
    fonts-dejavu-core \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage de développement
FROM base as development

# Installer des outils de développement supplémentaires
RUN pip install --no-cache-dir \
    pytest \
    black \
    flake8 \
    mypy

# Variables d'environnement pour le développement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=poll
ENV STREAMLIT_SERVER_RUN_ON_SAVE=true
ENV STREAMLIT_LOGGER_LEVEL=debug

# Créer les dossiers de données
RUN mkdir -p data/uploads data/processed data/exports

# Exposer le port Streamlit
EXPOSE 8501

# Commande de développement
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true", "--server.fileWatcherType", "poll", "--server.runOnSave", "true"]

# Stage de production
FROM base as production

# Copier le code de l'application
COPY . .

# Créer les dossiers de données
RUN mkdir -p data/uploads data/processed data/exports

# Variables d'environnement pour la production
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
ENV PYTHONUNBUFFERED=1

# Exposer le port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/healthz || exit 1

# Commande de production
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]