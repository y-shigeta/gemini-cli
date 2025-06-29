# overview

gemini cliでの並行開発

[gemini cli repo](https://github.com/google-gemini/gemini-cli?tab=readme-ov-file#quickstart)
[referenced note](https://zenn.dev/schroneko/articles/gemini-cli-tutorial)


# install

## gemini cli

```bash
npm install -g @google/gemini-cli
gemini -s --yolo -a
```

## byobu

```bash
brew install byobu
byobu
byobu list-sessions
byobu attach -t セッション名
```

|操作内容|キー|
|----|----|
|新しいウィンドウ|F2|
|ウィンドウ切替|F3/F4|
|ウィンドウ名変更|Shift+F8|
|分割（縦）|Ctrl+F2|
|分割（横）|Shift+F2|
|デタッチ|F6|
|設定メニュー|F9|


# usage

## sample usage
- Explore a new codebase
Start by cding into an existing or newly-cloned repository and running gemini.

> Describe the main pieces of this system's architecture.
> What security mechanisms are in place?

- Work with your existing code
> Implement a first draft for GitHub issue #123.
> Help me migrate this codebase to the latest version of Java. Start with a plan.

- Automate your workflows
Use MCP servers to integrate your local system tools with your enterprise collaboration suite.

> Make me a slide deck showing the git history from the last 7 days, grouped by feature and team member.


## git worktree
open -na Terminal

git worktree add -b feature/frontend ../frontend main
git worktree add -b feature/backend ../backend main
git worktree add -b feature/frontend ../frontend main
git worktree add -b feature/frontend ../frontend main
git worktree add src/notifier/ -b feat/notifier

git worktree remove ../frontend

# 並行開発


- 要件をもとに設計書を作成して
- 設計書に、機能仕様、IF仕様、シーケンスダイアグラム（Mermaidで作成）を追記して

- 
# reference
[claude](https://www.wantedly.com/companies/wantedly/post_articles/981006?source=ranking)
