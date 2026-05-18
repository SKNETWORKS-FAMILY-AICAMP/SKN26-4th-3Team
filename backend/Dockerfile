# @file Dockerfile
# @role
# Builds the Django backend runtime image and copies the application entrypoint and source tree.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /backend

# mysqlclient builds native extensions, so the image needs compiler and MySQL
# development headers only during dependency installation.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Normalize the entrypoint line endings because this repository is edited on
# Windows but the container executes the script with /bin/sh.
COPY docker-entrypoint.sh ./docker-entrypoint.sh
RUN sed -i 's/\r$//' ./docker-entrypoint.sh && \
    chmod +x ./docker-entrypoint.sh

COPY app ./app

EXPOSE 8000

# The entrypoint handles migrations, data loading, image sync, and optional
# Pinecone indexing before it starts the Django server.
CMD ["sh", "/backend/docker-entrypoint.sh"]

# ----------------------------------------------------------------
# Update History
# 2026-05-18: git diff 기준 @file/@role header, Docker build 단계 설명 주석, entrypoint 역할 주석, EOF footer 추가. (worker: @nobrain711)
# 2026-05-13: fix(docker): normalize startup script handling. (author: @nobrain711)
# 2026-05-13: fix(django): guard migrate schema drift. (author: @nobrain711)
# 2026-05-11: fix(docker): sync database credentials from env. (author: @nobrain711)
# 2026-05-11: feat(backend): migrate django fragrance apiAdds the Django REST backend, scent engine services, perfume data loa.... (author: @nobrain711)
# ----------------------------------------------------------------

# EOF: Dockerfile
