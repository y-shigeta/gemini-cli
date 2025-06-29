# trend-db サービス設計

## 1. IF 仕様

- MongoDB プロトコル
- trend-crawler, trend-api, notifier がクライアント

### 主なコレクション

| コレクション名 | 用途           |
| -------------- | -------------- |
| trends         | トレンド情報   |
| logs           | ログ・監査情報 |

## 2. 機能一覧

- トレンド情報の保存
- トレンド情報の検索・取得
- ログ・監査情報の保存

## 3. 機能仕様

- trends コレクションにトレンド情報を JSON で保存
- trend-api からのクエリで検索・集計
- trend-crawler, notifier からの書き込みを受け付け
