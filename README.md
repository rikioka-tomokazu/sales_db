# Gmail to BigQuery Email Processor

このプロジェクトは、Gmail APIを使用して特定のメールアドレス宛に届いたメールを取得し、正規表現および生成AIを用いてメール本文から各種情報を抽出・構造化し、BigQueryに蓄積する日次バッチ処理スクリプトです。

## 機能

1. Gmail APIを使用して `rc_support@frontier-gr.jp` 宛に届いたメールを取得
2. 正規表現を使用して以下の情報を抽出:
   - 法人名
   - URL
   - 業界
   - 設立年
   - 資本金
   - 売上
   - 決算月
   - 社員数
   - 所在地（都道府県）
   - 最寄り駅
   - 法人概要

3. 生成AIを活用して以下のカテゴリ情報を抽出:
   - 案件種別
   - 契約形態
   - 業界
   - 使用技術
   - 使用データ
   - 使用ツール・基盤
   - 担当フェーズ
   - 担当役割

4. 抽出した情報をBigQueryに登録
5. 日次バッチとして実行

## セットアップ

### 前提条件

- Python 3.8以上
- Google Cloud Platformのアカウント
- Gmail APIの有効化とOAuth 2.0クライアントIDの作成
- BigQueryのプロジェクト作成

### インストール

1. リポジトリをクローン:

```bash
git clone https://github.com/rikioka-tomokazu/sales_db.git
cd sales_db
```

2. 依存パッケージのインストール:

```bash
pip install -r requirements.txt
```

3. 環境変数の設定:

`.env.example` ファイルを `.env` にコピーし、必要な認証情報を設定します:

```bash
cp .env.example .env
```

`.env` ファイルを編集して以下の情報を設定:

```
# Gmail API credentials
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
GMAIL_TARGET_EMAIL=rc_support@frontier-gr.jp

# BigQuery credentials
GOOGLE_APPLICATION_CREDENTIALS=bigquery-credentials.json
BIGQUERY_PROJECT_ID=your-project-id
BIGQUERY_DATASET_ID=email_data
BIGQUERY_TABLE_ID=extracted_info

# OpenAI API key for AI extraction
OPENAI_API_KEY=your-openai-api-key
```

### Gmail API認証情報の取得

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを作成または選択
3. APIライブラリから「Gmail API」を有効化
4. 認証情報を作成 > OAuth 2.0クライアントID > デスクトップアプリケーション
5. JSONファイルをダウンロードし、`credentials.json`として保存

### BigQuery認証情報の取得

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを作成または選択
3. IAMと管理 > サービスアカウント > サービスアカウントを作成
4. BigQueryへのアクセス権を付与（BigQuery管理者ロール）
5. キーを作成（JSON形式）
6. ダウンロードしたJSONファイルを`bigquery-credentials.json`として保存

### OpenAI API Keyの取得

1. [OpenAI API](https://platform.openai.com/)にアクセス
2. アカウント作成・ログイン
3. APIキーを生成
4. `.env`ファイルの`OPENAI_API_KEY`に設定

## 使用方法

### 単発実行

特定の日数分のメールを処理する場合:

```bash
python src/main.py --days 7 --run-now
```

### 日次バッチとしてスケジュール実行

毎日特定の時間に実行するようにスケジュールする場合:

```bash
python src/main.py --schedule --hour 1 --minute 0
```

これにより、毎日午前1時にメール処理が実行されます。

### コマンドラインオプション

- `--days`: 過去何日分のメールを取得するか（デフォルト: 1）
- `--schedule`: 日次ジョブとしてスケジュール実行する
- `--hour`: 日次ジョブを実行する時間（24時間形式、デフォルト: 1）
- `--minute`: 日次ジョブを実行する分（デフォルト: 0）
- `--run-now`: ジョブを即時実行する

## ログ

ログは `email_processor.log` ファイルに記録されます。また、標準出力にも表示されます。

## トラブルシューティング

### Gmail API認証エラー

初回実行時にブラウザが開き、Googleアカウントへのアクセス許可を求められます。許可すると、`token.json`ファイルが生成され、以降の実行では自動的に認証されます。

### BigQuery接続エラー

- `GOOGLE_APPLICATION_CREDENTIALS`環境変数が正しく設定されているか確認
- サービスアカウントに適切な権限が付与されているか確認
- プロジェクトIDが正しいか確認

### OpenAI API呼び出しエラー

- APIキーが正しく設定されているか確認
- APIの利用制限に達していないか確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
