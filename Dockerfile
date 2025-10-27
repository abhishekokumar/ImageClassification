FROM python:3.9-slim

WORKDIR /app

# Install system dependencies + nginx + curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    nginx \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY frontend ./frontend/
COPY model ./model/
COPY server ./server/

# Configure nginx using EC2-style configuration
RUN echo 'server { \
    listen 80; \
    server_name _; \
    root /app/frontend; \
    index app.html; \
    \
    location /api/ { \
        rewrite ^/api(.*) $1 break; \
        proxy_pass http://127.0.0.1:5000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
        add_header Access-Control-Allow-Origin *; \
    } \
}' > /etc/nginx/sites-available/default

# Log to stdout/stderr
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Expose HTTP port
EXPOSE 80

# Copy start script to run Flask in background and nginx in foreground
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Start Flask and nginx
CMD ["/app/start.sh"]
