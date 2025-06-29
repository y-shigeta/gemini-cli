# Conversation Guidelines
常に日本語で会話する

# Development Philosophy

## Test-Driven Development (TDD)
- 原則としてテスト駆動開発（TDD）で進める
- 期待される入出力に基づき、まずテストを作成する
- 実装コードは書かず、テストのみを用意する
- テストを実行し、失敗を確認する
- テストが正しいことを確認できた段階でコミットする
- その後、テストをパスさせる実装を進める
- 実装中はテストを変更せず、コードを修正し続ける
- すべてのテストが通過するまで繰り返す

## Architecture
- Kubernetes上でマイクロサービスを構築する
- 一つのマイクロサービスは、一つのsrc/{feature}フォルダ配下でだけ作業を行うこと
- Dev環境は、src/{feature}フォルダに、DockerfileとDockercomposeで準備すること
- .gitignoreや.envなど必要なファイルは予め作成してください
