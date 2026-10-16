# 给所有外部 Agent

本仓库的漫剧、短剧和小说改编执行以下约定：

- 写剧本、资产说明、分镜和提示词时直接完成当前阶段。
- 制作方法使用 `.cursor/skills/workflow`；不得改用本仓库其他短剧技能。
- 执行前读取 `.cursor/rules/本地漫剧流程.mdc`，再按阶段读取 `workflow` 点名的 reference。
- 新制作项目开始时，先确认用户选择：已有 Toonflow 并使用画布、需要在 Windows 安装后使用画布，或不使用 Toonflow 直接本地制作；项目已有明确记录时不重复问。
- 已有画布时读取 `.cursor/skills/mcp-canvas-runtime/SKILL.md`，先调用 `getAppState`，再通过 MCP 正式工具操作当前项目和节点。
- 需要安装时读取 `.cursor/skills/toonflow-windows-setup/SKILL.md`：GitHub 可用则从官方仓库或 Release 安装；GitHub 不可用则只用可验证且允许分发的干净产物制作离线 Windows 包，严禁包含凭据和用户数据。
- 不使用画布时读取 `.cursor/skills/local-readable-runtime/SKILL.md`，以人类可读的中文目录和文件名保存，不创建画布 JSON 或 UUID-only 用户目录。
- 当前外部 Agent 是唯一文字大脑；不得调用 `runAgent` 委托内置 Agent。
- 画布模式不得直接修改带 `toonflowCanvas` 标记的 JSON；本地模式不得仿造画布节点结构。
- 正式资产设计前询问一次画风来源和可提供的角色、场景、道具、服装、站位或构图参考图；已有答案不重复问，用户可明确选择没有参考图。
- 图片和视频只使用当前执行模式真实提供的模型、配置、参考和生成函数。生成媒体前必须展示完整方案并取得明确授权；视频模型必须由用户指定。
- 视频提示词按用户指定模型路由：Seedance 2.0/2.5 执行 `workflow` 内嵌 PART A 和 A9；Vidu 先执行 `.cursor/skills/vidu-video-prompt/SKILL.md`，再由用户选择 Q2 或 Q3 并执行对应子技能；其他模型必须依据其当前官方规范。
- Vidu Q2 Pro Fast 只用于图生/首尾帧，多参考必须选择支持 Reference-to-Video 的型号；Q3 的 Pro/Fast/Turbo/Reference/Mix/Drama/Ad 也不得混用能力或模板。
- Seedance、Vidu Q2 和 Vidu Q3 正式提示词分别通过规则指定的专用校验脚本后才能交付或生成，画布/本地模式都不能跳过。

两种执行模式只改变布局、保存位置和工具入口，不降低或改写 `workflow` 的结果质量、正文格式和提示词模板。普通聊天无法读取仓库规则或写入项目；至少需要能打开本仓库、读取 Agent Skill 和写文件的编程环境，画布模式还必须支持 Streamable HTTP MCP。
