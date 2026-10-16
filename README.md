# AIGC 漫剧制作规则与 Toonflow 离线安装包

本包用于把同一套漫剧制作流程迁移到其他 Windows 电脑或其他编程 Agent。文字创作由当前 Agent 完成；用户可以选择 Toonflow 画布模式、安装后使用画布，或完全不使用 Toonflow 的本地目录模式。

首次交给新 Agent 时，直接复制发送根目录 `发给Agent的第一句话.txt` 的全文。

## 仓库内容

- `发给Agent的第一句话.txt`：适用于不会自动识别 `.cursor/skills` 的 Agent 的统一入口指令。
- `AGENTS.md`、`.cursor/`：项目规则、默认 workflow、v1.1.8 兼容 workflow、Seedance 内嵌路由、Vidu Q2/Q3 专用提示词、MCP 画布执行、本地可读执行和 Windows 安装技能。
- `MCP接入.md`：Toonflow MCP 接入说明。
- `Toonflow离线安装包/2.0.6/`：Windows 完整安装程序、许可证、安装说明和安装程序校验值。
- `配置模板/`：Cursor、Codex 和通用 Streamable HTTP MCP 配置示例，全部使用占位符，不含真实凭据。

## 安装规则与 Skills

克隆仓库后，可以直接把以下内容复制到目标项目根目录，并保留目录层级：

```text
目标项目/
├─ AGENTS.md
├─ MCP接入.md
└─ .cursor/
   ├─ rules/
   └─ skills/
```

不要只复制 `SKILL.md` 而遗漏 `references/` 和 `scripts/`。

### Cursor

Cursor 会读取项目中的 `AGENTS.md`、`.cursor/rules` 和 `.cursor/skills`。打开目标项目后新建对话，发送小说或剧情，入口规则会先询问三种执行方式。

### Codex 或其他编程 Agent

把同一目录复制到项目根目录，并在该 Agent 的项目指令中明确要求：

```text
开始漫剧制作前先读取 AGENTS.md 和 .cursor/rules/本地漫剧流程.mdc，
再按规则读取 .cursor/skills 下被点名的 SKILL.md 与 reference。
```

如果客户端不会自动识别 `.cursor/skills`，Agent 仍可把这些文件当作普通项目指令读取。

### 使用限制

- 本地目录模式只要求 Agent 能读取、写入项目文件并调用所需媒体工具。
- 画布模式还要求 Agent 支持 Streamable HTTP MCP、自定义请求头和本机地址访问。
- 普通网页聊天、普通豆包对话等不能读取项目文件或连接 MCP 的客户端，不能完整运行本包。
- 媒体模型和 API 凭据不在本包中，必须由使用者在目标环境自行合法配置。

## 三种入口

1. **已有 Toonflow，并使用画布**：配置 MCP 后，通过正式节点工具写入画布。
2. **没有 Toonflow，但需要安装后使用画布**：运行离线安装程序，启用 MCP，再进入画布模式。
3. **不使用 Toonflow**：直接建立人类可读的中文项目目录，不需要安装软件或配置 MCP。

三种布局模式使用同一 `workflow`、剧本规则、资产规则和验收关口；差异仅在保存布局和工具入口。视频提示词还会按用户指定模型分流：Seedance 2.0/2.5 使用内嵌 PART A/A9；Vidu 先经总路由，再由用户选择 Q2 或 Q3 及当前真实可用型号；其他模型必须读取其官方规范，不得混用模板。实际图片、视频质量仍取决于使用的真实媒体模型。

## 安全

本包不包含 API Key、MCP Bearer Token、用户项目、工作区、登录状态、缓存、日志或个人媒体。不要把自己配置后的 `settings.json`、`mcpRuntime*.json` 或用户级 MCP 配置重新打入公开包。

## 校验

安装程序的 SHA-256 校验清单位于：

```text
Toonflow离线安装包/2.0.6/SHA256SUMS.txt
```
