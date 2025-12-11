FROM python:3.12-slim

WORKDIR /app

# Créer un utilisateur non-root
RUN useradd -m appuser

COPY app.py .

RUN pip install --no-cache-dir flask

# Changer de propriétaire
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python3", "app.py"]
