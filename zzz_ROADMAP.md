# 🚀 YouTube Caption API デプロイ ロードマップ

YouTube動画の字幕をFastAPI経由で取得できるAPIをRailwayにデプロイするまでの手順です。

## 📋 現在の状況

| 項目 | 状態 |
|------|------|
| FastAPI + youtube-transcript-api コード | ✅ 完成 |
| GitHubリポジトリ | ✅ `c0rat1e5/__fastapi_youtube_script__` |
| uv + pyproject.toml 依存関係管理 | ✅ 完成 |
| .gitignore | ✅ 完成 |

---

## Phase 1: Docker化 🐳

### タスク一覧

| タスク | 説明 | 状態 |
|--------|------|------|
| `Dockerfile` 作成 | Python + uvicorn でAPIを起動 | ⬜ |
| `.dockerignore` 作成 | 不要ファイルを除外 | ⬜ |
| ローカルでビルド＆テスト | `docker build` → `docker run` で動作確認 | ⬜ |

### コマンド例

```bash
# Dockerイメージをビルド
docker build -t youtube-caption-api .

# コンテナを起動（ポート8000）
docker run -p 8000:8000 youtube-caption-api

# 動作確認
curl http://localhost:8000/
curl http://localhost:8000/caption/VgpTwJ-snGw?format=srt&language=ja
```

---

## Phase 2: Railway デプロイ準備 🛤️

### タスク一覧

| タスク | 説明 | 状態 |
|--------|------|------|
| 環境変数対応 | `PORT` 環境変数をコードで使用 | ⬜ |
| ヘルスチェック追加 | `/health` エンドポイント追加 | ⬜ |
| `railway.toml` 作成 (任意) | Railway固有の設定 | ⬜ |

### 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|-----------|
| `PORT` | APIサーバーのポート番号（Railwayが自動設定） | 8000 |

---

## Phase 3: Railway デプロイ 🌐

### タスク一覧

| タスク | 説明 | 状態 |
|--------|------|------|
| Railway アカウント作成 | https://railway.app でサインアップ | ⬜ |
| 新規プロジェクト作成 | "Deploy from GitHub repo" を選択 | ⬜ |
| GitHubリポジトリ連携 | `__fastapi_youtube_script__` を選択 | ⬜ |
| 自動デプロイ確認 | mainブランチへのpushで自動デプロイ | ⬜ |
| 公開URL取得 | `*.up.railway.app` 形式のURL | ⬜ |

### Railway デプロイ手順

1. **Railway にログイン**
   - https://railway.app にアクセス
   - GitHubアカウントでログイン

2. **新規プロジェクト作成**
   - 「New Project」をクリック
   - 「Deploy from GitHub repo」を選択
   - `c0rat1e5/__fastapi_youtube_script__` を選択

3. **デプロイ設定確認**
   - Railwayが自動でDockerfileを検出
   - 環境変数 `PORT` は自動設定される

4. **公開URL設定**
   - Settings → Networking → Generate Domain
   - `https://xxx.up.railway.app` 形式のURLが発行される

---

## Phase 4: 本番運用 🏭

### タスク一覧

| タスク | 説明 | 状態 |
|--------|------|------|
| 動作確認 | 公開URLでAPI動作テスト | ⬜ |
| n8n連携テスト | n8nワークフローから本番URL呼び出し | ⬜ |
| ログ・モニタリング | Railwayダッシュボードで確認 | ⬜ |
| レート制限追加 (任意) | YouTube API制限対策 | ⬜ |


---

## 📁 必要なファイル一覧

```
__fastapi_youtube_script__/
├── youtube_caption_api.py   ✅ 完成
├── test_api.py              ✅ 完成
├── zzz.py                   ✅ 完成
├── pyproject.toml           ✅ 完成
├── .gitignore               ✅ 完成
├── ROADMAP.md               ✅ 完成
├── Dockerfile               ⬜ 作成必要
├── .dockerignore            ⬜ 作成必要
└── README.md                ⬜ 推奨
```
