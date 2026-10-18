读取 `skills/ai-drama-harness/SKILL.md` 并按其流程启动 AI 短剧生产。

用户输入会包含以下信息之一：
- 飞书链接 + 上传剧本（模式 A）
- 仅上传剧本（模式 B，确认后才建表）

按 SKILL.md 中的启动协议和 Phase A/B 流程执行。调度下游 skill 时，先读取该 skill 的 SKILL.md。

牢记写入授权铁律：聊天中的意见/讨论只产生文字草案，任何 init/write/generate/push 必须先列出写入清单并得到用户明确确认；只读命令（read/pull/expand/status）可随时执行。

用户输入: $ARGUMENTS
