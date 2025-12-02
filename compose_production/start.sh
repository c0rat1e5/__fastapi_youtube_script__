#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

exec uv run uvicorn youtube_caption_api:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers ${WORKERS:-1}
