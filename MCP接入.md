# MCP 接入

本文只适用于选择“使用 Toonflow 画布”的项目。选择本地目录制作时不需要 MCP，按 `.cursor/skills/local-readable-runtime/SKILL.md` 保存，但创作规则和质量标准不变。

## Windows 尚未安装

- GitHub 可访问：使用官方仓库 <https://github.com/HBAI-Ltd/Toonflow-app> 或其官方 Release，按当前版本说明安装。
- GitHub 不可访问：使用来源可验证的官方安装包或干净构建产物制作离线包；必须排除用户项目、设置、API Key、MCP Token、缓存和日志。
- 详细操作和验收执行 `.cursor/skills/toonflow-windows-setup/SKILL.md`。

## 共同前提

1. 启动工作台并打开目标项目。
2. 在“设置 → MCP”启用服务。
3. 复制界面显示的实际 HTTP 地址和 Bearer 凭据。默认地址通常是 `http://127.0.0.1:10588/mcp`；端口被占用时以界面实际值为准。
4. 不把凭据提交到仓库。

外部 Agent 连接后先调用 `getAppState`，确认 `connectionId`、项目目录和当前画布。创作文字由外部 Agent 完成；不要调用 `runAgent`。

## Cursor

用户级配置文件：`%USERPROFILE%\.cursor\mcp.json`

```json
{
  "mcpServers": {
    "toonflow": {
      "url": "http://127.0.0.1:<实际端口>/mcp",
      "headers": {
        "Authorization": "Bearer <实际凭据>"
      }
    }
  }
}
```

保存后重新加载 MCP。

## Codex

配置文件：`%USERPROFILE%\.codex\config.toml`

```toml
[mcp_servers.toonflow]
url = "http://127.0.0.1:<实际端口>/mcp"
http_headers = { Authorization = "Bearer <实际凭据>" }
```

## 其他支持 Streamable HTTP MCP 的 Agent

使用同一地址，并设置请求头：

```text
Authorization: Bearer <实际凭据>
```

该 Agent 还必须能读取本仓库的：

- `AGENTS.md`
- `.cursor/rules/本地漫剧流程.mdc`
- `.cursor/skills/workflow/`
- `.cursor/skills/mcp-canvas-runtime/`
- `.cursor/skills/toonflow-windows-setup/`
- `.cursor/skills/local-readable-runtime/`
- `.cursor/skills/vidu-video-prompt/`
- `.cursor/skills/vidu-q2-video-prompt/`
- `.cursor/skills/vidu-q3-video-prompt/`

若客户端不会自动识别 `.cursor/skills`，应在其项目指令中明确要求先读取以上路径。

## 安全与切换

- 凭据只用于本机回环地址，不发送到远端仓库或聊天。
- 修改端口、重置凭据或多开应用后，从设置页重新复制实际配置。
- 同一时刻只允许一个 Agent 修改同一节点；切换 Agent 前等待当前写入或生成完成。
- 新 Agent 接管后重新调用 `getAppState` 和读取目标节点，不复用上一 Agent 缓存的节点 ID。
