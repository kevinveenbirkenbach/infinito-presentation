FROM python:slim

# Set working directory
WORKDIR /app

# Copy dependencies and install them
COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --timeout 60 -r requirements.txt

# (Optional) Installiere curl, falls es nicht bereits vorhanden ist
RUN apt-get update && apt-get install -y curl

# Copy application code
COPY ./ .

# Expose port
EXPOSE 5000

# Healthcheck: Prüft, ob die App über HTTP erreichbar ist
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://127.0.0.1:5000/ || exit 1

# Start the application
CMD ["python", "app.py"]