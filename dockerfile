# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Copy entry point scripts
COPY start-django.sh /code/start-django.sh
COPY start-celeryworker.sh /code/start-celeryworker.sh
COPY start-celerybeat.sh /code/start-celerybeat.sh

# Ensure the entrypoint scripts are executable
RUN chmod +x /code/start-django.sh /code/start-celeryworker.sh /code/start-celerybeat.sh
