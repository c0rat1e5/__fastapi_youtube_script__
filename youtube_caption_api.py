# -*- coding: utf-8 -*-
"""
YouTube字幕取得API - n8n用
FastAPIを使用してHTTP APIエンドポイントを提供

使い方:
  python youtube_caption_api.py

エンドポイント:
  GET /caption/{video_id}?format=srt&language=ja

n8nでの使用:
  HTTP Requestノードで http://localhost:8000/caption/VIDEO_ID を呼び出す
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, JSONFormatter, TextFormatter
import uvicorn

# .env ファイルを読み込み（ローカル開発用、なければスキップ）
load_dotenv()

app = FastAPI(
    title="YouTube Caption API",
    description="YouTube動画の字幕を取得するAPI（n8n連携用）",
    version="1.0.0",
)

# プロキシ設定（環境変数から取得）
# Webshare Residential用
WEBSHARE_PROXY_USERNAME = os.getenv("WEBSHARE_PROXY_USERNAME")
WEBSHARE_PROXY_PASSWORD = os.getenv("WEBSHARE_PROXY_PASSWORD")

# キャッシュ設定（秒）
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # デフォルト1時間

def create_ytt_api():
    """プロキシ設定付きの YouTubeTranscriptApi を作成"""
    if WEBSHARE_PROXY_USERNAME and WEBSHARE_PROXY_PASSWORD:
        from youtube_transcript_api.proxies import WebshareProxyConfig
        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=WEBSHARE_PROXY_USERNAME,
                proxy_password=WEBSHARE_PROXY_PASSWORD,
            )
        )
    return YouTubeTranscriptApi()

# APIインスタンス
ytt_api = create_ytt_api()

# シンプルなメモリキャッシュ（最大サイズ制限付き）
_cache = {}
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "100"))  # 最大100件

def get_cached_transcript(video_id: str, language: str):
    """キャッシュから字幕を取得、なければAPIから取得してキャッシュ"""
    import time
    cache_key = f"{video_id}:{language}"
    
    # キャッシュチェック
    if cache_key in _cache:
        cached_data, timestamp = _cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return cached_data
        else:
            # 期限切れは削除
            del _cache[cache_key]
    
    # キャッシュサイズ制限（古いものから削除）
    if len(_cache) >= CACHE_MAX_SIZE:
        # 最も古いエントリを削除
        oldest_key = min(_cache.keys(), key=lambda k: _cache[k][1])
        del _cache[oldest_key]
    
    # APIから取得
    transcript = ytt_api.fetch(video_id, languages=[language])
    _cache[cache_key] = (transcript, time.time())
    return transcript


@app.get("/")
def root():
    """APIの説明"""
    return {
        "message": "YouTube Caption API",
        "endpoints": {
            "/caption/{video_id}": "字幕を取得",
            "/languages/{video_id}": "利用可能な言語を取得",
            "/health": "ヘルスチェック",
        },
        "example_languages": "/languages/VgpTwJ-snGw",
        "example_caption": "/caption/VgpTwJ-snGw?format=srt&language=ja",
        "example_caption_full_text": "/caption/VgpTwJ-snGw/full_text?language=ja",
    }


@app.get("/health")
def health_check():
    """ヘルスチェック用エンドポイント"""
    return {"status": "healthy"}


@app.get("/languages/{video_id}")
def get_available_languages(video_id: str):
    """
    動画で利用可能な字幕言語のリストを取得
    """
    try:
        transcript_list = ytt_api.list(video_id)
        languages = []
        for transcript in transcript_list:
            languages.append(
                {
                    "language": transcript.language,
                    "language_code": transcript.language_code,
                    "is_generated": transcript.is_generated,
                    "is_translatable": transcript.is_translatable,
                }
            )
        return {"video_id": video_id, "languages": languages}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/caption/{video_id}")
def get_caption(
    video_id: str,
    format: str = Query(default="srt", description="出力形式: srt, json, text"),
    language: str = Query(default="ja", description="言語コード: ja, en, etc."),
):
    """
    YouTube動画の字幕を取得

    - **video_id**: YouTube動画ID（例: VgpTwJ-snGw）
    - **format**: 出力形式（srt, json, text）
    - **language**: 言語コード（ja, en など）
    """
    try:
        # 字幕を取得（キャッシュ付き）
        transcript = get_cached_transcript(video_id, language)

        # フォーマット変換
        if format == "srt":
            formatter = SRTFormatter()
            content = formatter.format_transcript(transcript)
            return PlainTextResponse(content, media_type="text/plain; charset=utf-8")

        elif format == "json":
            # 生データをJSON形式で返す
            data = []
            for snippet in transcript:
                # 新しいAPIではオブジェクト属性としてアクセス
                data.append(
                    {
                        "text": snippet.text,
                        "start": snippet.start,
                        "duration": snippet.duration,
                    }
                )
            return JSONResponse(
                {"video_id": video_id, "language": language, "transcript": data}
            )

        elif format == "text":
            formatter = TextFormatter()
            content = formatter.format_transcript(transcript)
            return PlainTextResponse(content, media_type="text/plain; charset=utf-8")

        else:
            raise HTTPException(status_code=400, detail=f"不明なフォーマット: {format}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/caption/{video_id}/full_text")
def get_full_text(
    video_id: str, language: str = Query(default="ja", description="言語コード")
):
    """
    字幕を1つのテキストとして取得（タイムスタンプなし）
    n8nでAI処理する場合に便利
    """
    try:
        # キャッシュ付きで取得
        transcript = get_cached_transcript(video_id, language)

        # すべてのテキストを結合（新しいAPIではオブジェクト属性としてアクセス）
        full_text = " ".join([snippet.text for snippet in transcript])

        return {"video_id": video_id, "language": language, "text": full_text}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    print("=" * 50)
    print("YouTube Caption API サーバー起動中...")
    print("=" * 50)
    print("\nn8nでの使用例:")
    print("  HTTP Requestノード → http://localhost:8000/caption/VIDEO_ID")
    print("\nエンドポイント:")
    print("  GET /caption/{video_id}?format=srt&language=ja")
    print("  GET /caption/{video_id}/full_text?language=ja")
    print("  GET /languages/{video_id}")
    print("\nドキュメント: http://localhost:8000/docs")
    print("=" * 50 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
