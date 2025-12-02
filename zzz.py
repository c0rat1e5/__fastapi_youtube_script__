# -*- coding: utf-8 -*-

# YouTube字幕をSRT形式で取得するスクリプト
# youtube-transcript-apiを使用（公開動画の字幕取得用）

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

# 対象の動画ID
VIDEO_ID = "VgpTwJ-snGw"


def main():
    print(f"=== 動画 {VIDEO_ID} の字幕を取得 ===\n")
    
    try:
        # APIインスタンスを作成
        ytt_api = YouTubeTranscriptApi()
        
        # 利用可能な字幕リストを取得
        transcript_list = ytt_api.list(VIDEO_ID)
        
        print("利用可能な字幕:")
        for transcript in transcript_list:
            print(f"  - {transcript.language} ({transcript.language_code})")
            print(f"    自動生成: {transcript.is_generated}")
            print(f"    翻訳可能: {transcript.is_translatable}")
        
        # 日本語字幕を取得（自動生成含む）
        print(f"\n=== 日本語字幕をSRT形式で取得 ===\n")
        transcript = ytt_api.fetch(VIDEO_ID, languages=['ja'])
        
        # SRT形式に変換
        formatter = SRTFormatter()
        srt_content = formatter.format_transcript(transcript)
        
        # ファイルに保存
        output_file = f"caption_{VIDEO_ID}.srt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(srt_content)
        print(f"保存完了: {output_file}")
        
        # 最初の部分を表示
        print("\n=== SRT内容（最初の1000文字） ===\n")
        print(srt_content[:1000])
        
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
