
FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install --upgrade pip && \
    python -m pip install "torch==2.14.1+cpu" \
        --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install -r /tmp/requirements.txt && \
    python -m pip check

COPY . /app

CMD ["sleep", "infinity"]