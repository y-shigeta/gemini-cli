# notifier サービス設計

## 1. IF 仕様

- REST API（例: /notify, /health）
- Slack Webhook への POST
- trend-crawler, trend-api からの HTTP リクエスト受信

### エンドポイント例

| メソッド | パス    | 説明           |
| -------- | ------- | -------------- |
| POST     | /notify | Slack 通知実行 |
| GET      | /health | ヘルスチェック |

## 2. 機能一覧

- Slack 通知の送信
- 通知内容の整形
- 通知履歴の保存（オプション）

## 3. 機能仕様

- /notify で受け取った内容を Slack Webhook に POST
- 通知内容は JSON で受信し、メッセージを整形して送信
- /health で稼働確認
