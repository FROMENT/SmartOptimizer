# SmartOptimizer Docker Image
FROM python:3.9-slim

# Métadonnées
LABEL maintainer="SmartOptimizer Team"
LABEL description="Optimiseur intelligent de fichiers pour macOS/Linux"
LABEL version="1.0.0"

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    file \
    findutils \
    coreutils \
    git \
    && rm -rf /var/lib/apt/lists/*

# Créer l'utilisateur non-root
RUN useradd -m -u 1000 optimizer
USER optimizer
WORKDIR /home/optimizer

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --user --no-cache-dir -r requirements.txt

# Copier le code source
COPY --chown=optimizer:optimizer src/ ./src/
COPY --chown=optimizer:optimizer scripts/ ./scripts/
COPY --chown=optimizer:optimizer README.md ./

# Rendre les scripts exécutables
RUN chmod +x scripts/*.sh
RUN chmod +x src/analyzers/*.py
RUN chmod +x src/optimizers/*.py
RUN chmod +x src/reorganizers/*.py
RUN chmod +x src/utils/*.py

# Créer les répertoires de travail
RUN mkdir -p ./data ./backups ./reports

# Point d'entrée principal
COPY --chown=optimizer:optimizer docker/entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Volumes pour les données utilisateur
VOLUME ["/home/optimizer/data", "/home/optimizer/backups"]

# Port pour le serveur web (futur)
EXPOSE 8080

# Commande par défaut
ENTRYPOINT ["./entrypoint.sh"]
CMD ["overview"]