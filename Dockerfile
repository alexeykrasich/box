# Automation Control System - Production Docker Image
FROM python:3.12-slim

# Security: Don't run as root
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY server/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ ./

# Create scripts directory
RUN mkdir -p scripts && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Non-sensitive environment defaults (sensitive values via docker-compose or runtime)
ENV HOST=0.0.0.0
ENV PORT=5000
ENV DEBUG=false

# Run the application
CMD ["python", "app.py"]
