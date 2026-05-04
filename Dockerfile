FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget curl gnupg xvfb x11vnc fluxbox websockify novnc \
    libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 libdrm2 \
    libxkbcommon0 libgtk-3-0t64 libgbm1 libasound2t64 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

COPY . .

EXPOSE 7860

1CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
