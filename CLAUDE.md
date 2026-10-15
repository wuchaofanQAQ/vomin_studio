# Vomin Studio — AI 短剧生产底座

本项目是 AI 短剧全自动生产流水线：9 个 skill + CLI 执行层 + 飞书多维表格。

## 快速上手

用户说以下任一形式即触发全自动流程：
- "飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz，想法: ..."
- "剧名: xxx，想法: ..."
- "从想法起一部剧"、"建角色档案"、"拆分镜" 等触发词

收到后，读取 `skills/ai-drama-harness/SKILL.md` 按其流程编排。

## Skill 清单

| Skill | 路径 | 触发词 |
|---|---|---|
| ai-drama-harness | `skills/ai-drama-harness/SKILL.md` | 飞书链接+想法、从想法起一部剧 |
| story-developer | `skills/story-developer/SKILL.md` | 完善剧本设定和大纲 |
| character-bible-extractor | `skills/character-bible-extractor/SKILL.md` | 建角色档案、从剧本提取角色 |
| character-three-view-prompt | `skills/character-three-view-prompt/SKILL.md` | 出角色三视图 |
| scene-image-prompt | `skills/scene-image-prompt/SKILL.md` | 出场景空镜 |
| episode-generator | `skills/episode-generator/SKILL.md` | 写下一集、续写第X集 |
| storyboard-generator | `skills/storyboard-generator/SKILL.md` | 拆分镜 |
| battle-fx-storyboard | `skills/battle-fx-storyboard/SKILL.md` | 拆战斗戏、战斗特效分镜 |
| video-shot-prompt | `skills/video-shot-prompt/SKILL.md` | 转视频提示词 |

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
