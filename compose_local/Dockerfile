# syntax=docker/dockerfile:1.4

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_PREFERENCE=system \
    PORT=8765

# 必要最小限のパッケージ
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存関係をコピー＆インストール
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-cache

# アプリケーションコード
COPY youtube_caption_api.py ./

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}

CMD ["sh", "-c", "uv run uvicorn youtube_caption_api:app --host 0.0.0.0 --port ${PORT}"]
