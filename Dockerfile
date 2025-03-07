# Use Python 3.11.7 slim image
FROM python:3.11.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=5002

# Expose port
EXPOSE 5002

# Run the application
CMD ["gunicorn", "app:app", "--workers=4", "--worker-class=gevent", "--bind=0.0.0.0:5002", "--timeout=30"]
