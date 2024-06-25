# Use the official Python image from the Docker Hub
FROM python:3.10.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Change to production as needed
ENV DJANGO_ENVIRONMENT development

# Set work directory
WORKDIR /code

# Install system dependencies including PostgreSQL client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    default-mysql-client \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Set entrypoint script executable permissions
RUN chmod +x ./entrypoint.sh ./wait-for-db.sh

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["./entrypoint.sh"]

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
