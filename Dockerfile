FROM python:3.12-slim

# Install system dependencies for Playwright + virtual display
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    xvfb \
    x11vnc \
    fluxbox \
    websockify \
    novnc \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy all app files
COPY . .

# Expose port
EXPOSE 7860

# Start the API server
CMD ["python", "server.py"]
