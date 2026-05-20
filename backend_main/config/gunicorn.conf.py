# Gunicorn configuration for OCR Service
# Optimized for Docker Swarm with 2 replicas

# Core settings
bind = "0.0.0.0:8000"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"

# Timeouts (OCR + AI processing can take time)
timeout = 240
graceful_timeout = 30
keepalive = 5

# Memory & Performance
max_worker_memory = 512 * 1024 * 1024  # 512MB per worker
max_requests = 2000
max_requests_jitter = 200
preload_app = True
worker_tmp_dir = "/dev/shm"

# Logging (stdout/stderr for Docker)
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)s'

# Reverse proxy support (for nginx/traefik)
forwarded_allow_ips = "*"
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}
