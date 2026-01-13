# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL files
COPY . .

# Expose port (Railway uses $PORT)
EXPOSE 5000

# Run the application
CMD ["sh", "-c", "cd backend && gunicorn app:app --bind 0.0.0.0:$PORT --workers=2 --threads=4 --timeout=120"]
