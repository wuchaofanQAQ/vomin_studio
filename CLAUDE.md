# Vomin Studio — AI 短剧生产底座

本项目是 AI 短剧生产流水线：9 个 skill + CLI 执行层 + 飞书多维表格。输入为用户上传的小说章节或剧本。

## 快速上手

用户说以下任一形式即触发全自动流程：
- "飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz，剧本: （上传剧本）"
- "剧本: （上传剧本文件）"
- "剧本初始化"、"导入剧本"、"拆分镜" 等触发词

收到后，读取 `skills/ai-drama-harness/SKILL.md` 按其流程编排。

## 生图工作台直接出图

用户说「**生图工作台现在开始工作**」即视为对当前工作台待生成任务的授权，直接执行：

```bash
python cli.py workbench <WS>
```

执行前用一行汇总要跑的任务（条数 + 每行提示词首句 + 画面比例），然后开跑。生成完成后 `结果路径` 与 `状态` 自动回填到飞书工作台。

**续生**：用户在新行里用 `{生图工作台：任务名}` 引用上一条结果图继续生成——所以要做"接着改"的任务，**请填任务名**（任务名留空时按提示词首行前 20 字派生，不好引用）。

工作台字段：`任务名`（可空）、`提示词`（必填，可含 `{}`）、`模型`、`分辨率`、`画面比例`（三个都是下拉，留空走默认）、`状态`、`结果路径`、`备注`。默认值：模型 `ark.image_model`、分辨率 `2K`、比例 `16:9`。

## 核心纪律

聊天归聊天，写入归写入：用户在对话中的意见/讨论/否定只产生文字草案；任何 `init`/`write`/`generate`/`push` 动作都必须先列出写入清单、拿到用户明确确认后执行。只读命令（read/pull/expand/status）无需确认。

## Skill 清单

| Skill | 路径 | 触发词 |
|---|---|---|
| ai-drama-harness | `skills/ai-drama-harness/SKILL.md` | 飞书链接+上传剧本、剧本初始化 |
| drama-initializer | `skills/drama-initializer/SKILL.md` | 剧本初始化、导入剧本、导入小说、上传剧本 |
| novel-to-script | `skills/novel-to-script/SKILL.md` | 小说转剧本、转化小说章节、改编小说 |
| character-three-view-prompt | `skills/character-three-view-prompt/SKILL.md` | 出角色三视图 |
| script-to-scene-assets | `skills/script-to-scene-assets/SKILL.md` | 剧本抽场景、场景图提示词、母版/主场景/局部、图间关联 |
| novel-to-character-assets | `skills/novel-to-character-assets/SKILL.md` | 小说抽角色、新角色识别、补角色档案 |
| director-segment-prompt | `skills/director-segment-prompt/SKILL.md` | 拆分镜、分镜脚本、视频提示词、CLIP、导演级分段提示词 |

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
