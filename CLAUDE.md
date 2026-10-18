# Vomin Studio — AI 短剧生产底座

本项目是 AI 短剧生产流水线：6 个 skill + CLI 执行层 + 飞书多维表格。输入为用户上传的剧本。

## 快速上手

用户说以下任一形式即触发全自动流程：
- "飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz，剧本: （上传剧本）"
- "剧本: （上传剧本文件）"
- "剧本初始化"、"导入剧本"、"拆分镜" 等触发词

收到后，读取 `skills/ai-drama-harness/SKILL.md` 按其流程编排。

## 核心纪律

聊天归聊天，写入归写入：用户在对话中的意见/讨论/否定只产生文字草案；任何 `init`/`write`/`generate`/`push` 动作都必须先列出写入清单、拿到用户明确确认后执行。只读命令（read/pull/expand/status）无需确认。

## Skill 清单

| Skill | 路径 | 触发词 |
|---|---|---|
| ai-drama-harness | `skills/ai-drama-harness/SKILL.md` | 飞书链接+上传剧本、剧本初始化 |
| drama-initializer | `skills/drama-initializer/SKILL.md` | 剧本初始化、导入剧本、上传剧本 |
| character-bible-extractor | `skills/character-bible-extractor/SKILL.md` | 深化角色档案、从剧本提取角色 |
| character-three-view-prompt | `skills/character-three-view-prompt/SKILL.md` | 出角色三视图 |
| scene-image-prompt | `skills/scene-image-prompt/SKILL.md` | 出场景空镜 |
| storyboard-prompt | `skills/storyboard-prompt/SKILL.md` | 拆分镜、分镜脚本、视频提示词、CLIP |

## 使用规则

1. 收到触发词后，先读取对应 skill 的 SKILL.md，严格按其 Workflow 执行
2. harness 调度下游 skill 时，也要先读取该 skill 的 SKILL.md
3. 所有飞书读写通过 `python cli.py` 执行，不直接调用 Python 模块
4. 使用手册：`skills/AI短剧生产底座使用手册.md`

## 不要修改的文件

- `vomin/ark/client.py`
- `vomin/ark/image.py`
- `vomin/ark/video.py`
- `vomin/tts/doubao.py`
