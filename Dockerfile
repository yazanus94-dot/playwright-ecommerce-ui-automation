FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for Playwright browsers
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium firefox webkit

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start the application
CMD ["python", "app/main.py"]
