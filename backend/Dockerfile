# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be required by Python packages
# For example, build-essential for compiling some packages, or libpq-dev for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application source code into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (can be overridden in docker-compose)
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
# Note: For production, you might want to set FLASK_ENV=production

# Run main.py when the container launches
# Use gunicorn for a production-ready server
# The number of workers can be tuned based on the server's CPU cores
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.main:create_app()"]
