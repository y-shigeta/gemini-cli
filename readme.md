# overview

gemini cdk

[reference](https://zenn.dev/schroneko/articles/gemini-cli-tutorial)

# install

npm install -g @google/gemini-cli

vi ~/.gemini/settings.json

gemini -p "search top new today at japan"

gemini -p "search top 3 news today at japan" |
gemini -p "Please translate to Japanese and Enligsh"

# install markdownnify

git clone https://github.com/zcaceres/markdownify-mcp.git
npm install -g pnpm
pnpm install
pnpm run build
pnpm start

```yaml
"mcpServers":
  {
    "markdownify":
      {
        "command": "node",
        "args": ["/Users/yas/vscode/05_gemini/markdownify-mcp/dist/index.js"],
        "env":
          {
            // By default,
            ? the server will use the default install location of `uv`
              "UV_PATH"
            : "/Users/yas/.local/bin/uv",
          },
      },
  }
```

# 
# reference
[claude](https://www.wantedly.com/companies/wantedly/post_articles/981006?source=ranking)
