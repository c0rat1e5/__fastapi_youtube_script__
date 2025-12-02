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

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, JSONFormatter, TextFormatter
import uvicorn

app = FastAPI(
    title="YouTube Caption API",
    description="YouTube動画の字幕を取得するAPI（n8n連携用）",
    version="1.0.0"
)

# APIインスタンス
ytt_api = YouTubeTranscriptApi()


@app.get("/")
def root():
    """APIの説明"""
    return {
        "message": "YouTube Caption API",
        "endpoints": {
            "/caption/{video_id}": "字幕を取得",
            "/languages/{video_id}": "利用可能な言語を取得"
        },
        "example": "/caption/VgpTwJ-snGw?format=srt&language=ja"
    }


@app.get("/languages/{video_id}")
def get_available_languages(video_id: str):
    """
    動画で利用可能な字幕言語のリストを取得
    """
    try:
        transcript_list = ytt_api.list(video_id)
        languages = []
        for transcript in transcript_list:
            languages.append({
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable
            })
        return {"video_id": video_id, "languages": languages}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/caption/{video_id}")
def get_caption(
    video_id: str,
    format: str = Query(default="srt", description="出力形式: srt, json, text"),
    language: str = Query(default="ja", description="言語コード: ja, en, etc.")
):
    """
    YouTube動画の字幕を取得
    
    - **video_id**: YouTube動画ID（例: VgpTwJ-snGw）
    - **format**: 出力形式（srt, json, text）
    - **language**: 言語コード（ja, en など）
    """
    try:
        # 字幕を取得
        transcript = ytt_api.fetch(video_id, languages=[language])
        
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
                data.append({
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration
                })
            return JSONResponse({
                "video_id": video_id,
                "language": language,
                "transcript": data
            })
        
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
    video_id: str,
    language: str = Query(default="ja", description="言語コード")
):
    """
    字幕を1つのテキストとして取得（タイムスタンプなし）
    n8nでAI処理する場合に便利
    """
    try:
        transcript = ytt_api.fetch(video_id, languages=[language])
        
        # すべてのテキストを結合（新しいAPIではオブジェクト属性としてアクセス）
        full_text = " ".join([snippet.text for snippet in transcript])
        
        return {
            "video_id": video_id,
            "language": language,
            "text": full_text
        }
    
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
