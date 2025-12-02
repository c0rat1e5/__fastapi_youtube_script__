# Railway Production 使い方

## デプロイ方法

1. Railway にログイン: https://railway.app
2. New Project → Deploy from GitHub repo
3. `c0rat1e5/__fastapi_youtube_script__` を選択
4. Railway が自動で `compose_production/railway.toml` を検出

## ファイル構成

```
compose_production/
├── Dockerfile      # 本番用 Docker イメージ
├── railway.toml    # Railway 設定
├── start.sh        # 起動スクリプト
└── README.txt      # このファイル
```

## 環境変数（Railway で設定）

| 変数名    | 説明               | デフォルト |
|-----------|--------------------|-----------|
| PORT      | APIポート（自動設定）| 8000      |
| WORKERS   | uvicorn workers    | 1         |

## nginx/traefik について

不要。Railway が自動で以下を提供:
- HTTPS/SSL 終端
- ロードバランシング
- リバースプロキシ

## 本番 URL

デプロイ後: https://xxx.up.railway.app/

## ヘルスチェック

Railway は `/health` を自動監視
