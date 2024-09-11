# Use the official Python image from the Docker Hub, supporting multiple architectures
FROM python:3.10.12-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Change to production as needed
ENV DJANGO_ENVIRONMENT=production

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies and clients for PostgreSQL and MySQL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    pkg-config \
    postgresql-client \
    libmariadb-dev-compat \
    libmariadb-dev \
    default-mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy over the container the requirements.txt file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install all the app required packages
RUN pip install -r requirements.txt

# Copy project and settings template
COPY . /usr/src/app
COPY ./project/settings /usr/src/app/project/settings-template

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]