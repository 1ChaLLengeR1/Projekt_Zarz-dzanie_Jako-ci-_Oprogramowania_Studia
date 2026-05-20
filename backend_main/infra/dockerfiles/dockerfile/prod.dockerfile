FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app/

RUN pip install uv && uv pip install --system --no-cache ".[prod]"

COPY config/gunicorn.conf.py /app/config/gunicorn.conf.py

CMD ["gunicorn", "main:app", "-c", "config/gunicorn.conf.py"]