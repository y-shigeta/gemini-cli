# 目的
- Xをキーワードでトレンドを収集して表示させるモバイルアプリを作成したい

# 要求事項
- マイクロサービスで作成する前提で、機能を分割して欲しい。
- 各機能はDockerファイルにまとめてください。ローカルではDockerComposeで実行できるようにしてください。
- バックエンドはPython、FrontendはVueとTypeScriptで作ってもらいたい。
- まずは各々を適切なマイクロサービスに分割して、それぞれ各サービスの連携する設計書を作成してください。例えば、Xのトレンド収集、トレンド情報をNoSQLに保存する機能、トレンド情報を表示して可視化して表示するフロントエンド、トレンド情報をslackに通知する機能
