# Base image for Python
FROM python:slim

# Set working directory
WORKDIR /app

# Copy dependencies and install them
COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --timeout 60 -r requirements.txt

# Copy application code
COPY ./ .

# Expose port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
