# Gmail to BigQuery Email Processor - プロジェクト概要

## プロジェクト構成

### コアコンポーネント

| ファイル | 説明 |
|---------|------|
| `src/gmail_client.py` | Gmail APIを使用してメールを取得するクライアント |
| `src/email_parser.py` | 正規表現とAIを使用してメール本文から情報を抽出するパーサー |
| `src/bigquery_client.py` | 抽出した情報をBigQueryに登録するクライアント |
| `src/main.py` | 日次バッチ処理のメインスクリプト |

### 設定ファイル

| ファイル | 説明 |
|---------|------|
| `.env.example` | 環境変数のテンプレート |
| `.env` | 実際の環境変数設定ファイル（gitignoreに含まれる） |
| `requirements.txt` | 必要なPythonパッケージのリスト |

### スクリプト

| ファイル | 説明 |
|---------|------|
| `run_daily_job.sh` | 日次バッチジョブを実行するシェルスクリプト |
| `init_project.sh` | プロジェクトの初期設定を行うスクリプト |
| `verify_setup.py` | セットアップが正しく行われているか確認するスクリプト |

### テスト

| ファイル | 説明 |
|---------|------|
| `test_parser.py` | メールパーサーのテストスクリプト（OpenAI API使用） |
| `test_regex.py` | 正規表現抽出のみのテストスクリプト |

### デプロイメント

| ファイル | 説明 |
|---------|------|
| `Dockerfile` | Dockerコンテナ構築用設定ファイル |
| `docker-compose.yml` | Docker Composeによるデプロイメント設定 |
| `crontab_example.txt` | cronによるスケジューリング設定例 |

### ドキュメント

| ファイル | 説明 |
|---------|------|
| `README.md` | プロジェクトの概要、セットアップ方法、使用方法の説明 |
| `PROJECT_SUMMARY.md` | プロジェクト構成の詳細な説明（本ファイル） |

## 使用方法

### 初期セットアップ

```bash
# プロジェクトの初期化
./init_project.sh

# 環境変数の設定
# .envファイルを編集して必要な認証情報を設定

# セットアップの確認
python verify_setup.py
```

### 実行方法

```bash
# 単発実行（過去7日分のメールを処理）
python src/main.py --days 7 --run-now

# 日次バッチとしてスケジュール実行（毎日午前1時に実行）
python src/main.py --schedule --hour 1 --minute 0

# シェルスクリプトによる実行
./run_daily_job.sh
```

### Dockerによる実行

```bash
# Dockerイメージのビルドと実行
docker-compose up -d
```

## データフロー

1. Gmail APIを使用して `rc_support@frontier-gr.jp` 宛に届いたメールを取得
2. 正規表現を使用して法人情報を抽出
   - 法人名、URL、業界、設立年、資本金、売上、決算月、社員数、所在地、最寄り駅、法人概要
3. OpenAI APIを使用して案件情報を抽出
   - 案件種別、契約形態、業界、使用技術、使用データ、使用ツール・基盤、担当フェーズ、担当役割
4. 抽出した情報をBigQueryに登録
5. 日次バッチとして実行

## 認証情報

以下の認証情報が必要です：

1. Gmail API認証情報（OAuth 2.0クライアントID）
2. BigQuery認証情報（サービスアカウントキー）
3. OpenAI API Key（生成AI抽出用）

これらの認証情報は `.env` ファイルで管理します。
