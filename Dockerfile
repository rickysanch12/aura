FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install -e .

# Create necessary directories
RUN mkdir -p /app/logs ~/.alcos

# Expose ports
EXPOSE 8000 3000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ALCOS_LOG_FILE=/app/logs/alcos.log

# Run the API server
CMD ["python", "-m", "alcos.api.server"]
