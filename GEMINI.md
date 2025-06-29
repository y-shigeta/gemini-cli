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
- 各マイクロサービス間はAPIで通信し、疎結合であること
- KustomizeでManifestの環境分離を行うこと
- Github actionsでCICDを構築すること
- Bazelを利用してコンテナのビルドを高速化すること
- Git feature flowを採用すること
- src/{feature}フォルダに、DockerfileとDockercomposeを準備し、ローカルPCで開発を行うこと
- 各マイクロサービスは、src/{feature}フォルダに対応する。そのフォルダだけで開発を完結できること

## Others
- src/{feature}フォルダに、.gitignoreや.envなど必要なファイルは予め作成してください
