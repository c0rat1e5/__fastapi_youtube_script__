# ベースイメージ
FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 環境変数
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8765

# システム依存パッケージ（必要最小限）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv をインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 依存関係ファイルをコピー
COPY pyproject.toml uv.lock* ./

# 依存関係をインストール
RUN uv sync --frozen --no-dev --no-cache

# アプリケーションコードをコピー
COPY youtube_caption_api.py ./

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# ポート公開
EXPOSE ${PORT}

# 起動コマンド
CMD ["sh", "-c", "uv run uvicorn youtube_caption_api:app --host 0.0.0.0 --port ${PORT}"]
