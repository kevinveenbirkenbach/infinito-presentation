# Basis-Image für Python
FROM python:slim

ARG CYMAIS_REPOSITORY_PATH

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY app/ .

# Copy CyMaIS Code
COPY CYMAIS_REPOSITORY_PATH ./cymais-code

# Port freigeben
EXPOSE 5000

# Startbefehl
CMD ["python", "app.py"]
