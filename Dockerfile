# Basis-Image für Python
FROM python:slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY ./ .

# Port freigeben
EXPOSE 5000

# Startbefehl
CMD ["python", "app.py"]
