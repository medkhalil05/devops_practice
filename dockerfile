FROM python:3.11-slim

# Installer les dépendances système nécessaires pour speedtest-cli
RUN apt-get update && apt-get install -y \
    gcc \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier d'abord le requirements.txt pour mieux utiliser le cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY app.py .

# Créer un utilisateur non-root pour plus de sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]