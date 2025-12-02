# -*- coding: utf-8 -*-
"""
APIテスト用スクリプト
サーバーなしで直接字幕取得をテスト
"""

import requests

# APIベースURL
BASE_URL = "http://localhost:8000"

def test_full_text():
    """全文テキスト取得のテスト"""
    video_id = "VgpTwJ-snGw"
    url = f"{BASE_URL}/caption/{video_id}/full_text?language=ja"
    
    print(f"リクエスト: {url}")
    print("-" * 50)
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"ステータス: {response.status_code}")
        print(f"動画ID: {data['video_id']}")
        print(f"言語: {data['language']}")
        print(f"\n字幕テキスト（最初500文字）:")
        print(data['text'][:500])
        
    except requests.exceptions.ConnectionError:
        print("エラー: サーバーに接続できません")
        print("先にAPIサーバーを起動してください:")
        print("  python youtube_caption_api.py")
    except Exception as e:
        print(f"エラー: {e}")


def test_json_format():
    """JSON形式取得のテスト"""
    video_id = "VgpTwJ-snGw"
    url = f"{BASE_URL}/caption/{video_id}?format=json&language=ja"
    
    print(f"\nリクエスト: {url}")
    print("-" * 50)
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"ステータス: {response.status_code}")
        print(f"字幕セグメント数: {len(data['transcript'])}")
        print(f"\n最初の5セグメント:")
        for i, seg in enumerate(data['transcript'][:5]):
            print(f"  {i+1}. [{seg['start']:.2f}s] {seg['text']}")
        
    except requests.exceptions.ConnectionError:
        print("エラー: サーバーに接続できません")
    except Exception as e:
        print(f"エラー: {e}")


def test_languages():
    """利用可能言語一覧のテスト"""
    video_id = "VgpTwJ-snGw"
    url = f"{BASE_URL}/languages/{video_id}"
    
    print(f"\nリクエスト: {url}")
    print("-" * 50)
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"ステータス: {response.status_code}")
        print(f"利用可能な言語:")
        for lang in data['languages']:
            print(f"  - {lang['language']} ({lang['language_code']}) - 自動生成: {lang['is_generated']}")
        
    except requests.exceptions.ConnectionError:
        print("エラー: サーバーに接続できません")
    except Exception as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("YouTube Caption API テスト")
    print("=" * 50)
    
    test_languages()
    test_full_text()
    test_json_format()
