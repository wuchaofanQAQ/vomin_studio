---
name: story-developer
description: 从一个模糊的想法/一句话概念（logline），扩写并完善成完整的"剧本设定 + 全集剧情大纲"。当用户给出一句创意、主题、题材、人设或"我想拍个 XX 的短剧"这类不完整想法，需要把它发展成可落地的世界观、主线、人物和分集剧情大纲时使用。本 skill 产出文字设定与大纲，不直接出分集剧本（那交给 episode-generator）。
---

# Story Developer

## Overview

把用户的一句话/模糊想法，发展成一部短剧的**两大全局资产**：剧本设定 + 全集剧情大纲。产出的是"北极星"级文档——之后角色档案、分集剧本、场景画风全部以此为据。

## Workflow

### Step 1 — 澄清想法

读取用户的模糊想法，识别其中已有的要素与缺口。若想法缺失以下关键项，用 `references/clarify.md` 的清单**一次性追问**（不逐条轰炸）：

- 题材/类型（都市、古装、仙侠、悬疑…）
- 核心设定（核心冲突 / 金手指 / 世界观亮点）
- 主角身份与人设方向
- 目标时长与集数（例：30 集×2 分钟/集）
- 基调（爽、虐、甜、燃…）

用户未答的项：用类型惯例补全并在文档中标注"默认设定"，不擅自停摆。

### Step 2 — 生成剧本设定（全局资产）

按 `references/setting-template.md` 输出完整剧本设定，必须含：

1. 剧名 + 一句话卖点（logline）
2. 题材类型与定位（含受众、平台调性）
3. 基调（爽/虐/甜…）
4. 剧情简介（一句话 + 300字 + 世界观规则）
5. 主线与冲突（主冲突、目标、对抗力量）
6. **画面风格**（画风/色调/光影/质感）——★ 直接喂给三视图、场景 skill
7. 剧本节奏（钩子密度、爽点频率、单集时长、目标集数）
8. 剧本看点 / 爽点清单
9. 主要角色清单（仅列清单，详细档案交 character-bible-extractor）

> 完整字段逐节见 `references/setting-template.md`（12 节剧集圣经模板）。

### Step 3 — 生成全集剧情大纲

按 `references/outline-template.md` 输出全集剧情大纲：

- **剧情弧线**：起承转合、每 1/4 段的节点（激励事件、中点转折、低谷、高潮、结局）
- **分集大纲**：逐集一行——本集核心事件 + 出场角色 + 集末钩子（尤其短剧，每集结尾必须有钩子）
- 每集控制在"可被 episode-generator 消费"的粒度：事件明确、不写对白细节

大纲的结构骨架应服务叙事理论（参考 `references/outline-template.md` 的结构标注）：
- **三幕结构**：第一幕建置（~25%）、第二幕对抗（~50%）、第三幕解决（~25%），每幕之间有明确的情节点（Plot Point）
- **激励事件**（约 10-15% 处）：打破主角日常平衡、启动故事的事件
- **中点转折**（约 50% 处）：伪胜利或伪失败，劈开第二幕上下半
- **低谷**（约 75% 处）：主角跌入最低点
- **高潮**（约 85-90% 处）：核心冲突正面对决
- **情绪曲线**：铺垫→升温→爆发→回落，全程高潮=没有高潮

### Step 4 — 输出与说明

输出两大文档，附 2–3 行说明：哪些项来自用户想法、哪些是默认设定、画风基调如何定。用户修正 → 更新对应段落并重新输出受影响部分。

## 产出交接（重要）

本 skill 产出应明确标注两个下游入口：
- 角色档案 → 交给 `character-bible-extractor`
- 分集剧本 → 交给 `episode-generator`

## References

- `references/clarify.md` — 澄清问题清单（Step 1 用）
- `references/setting-template.md` — 剧本设定文档模板（Step 2 用）
- `references/outline-template.md` — 全集剧情大纲模板（Step 3 用）

## Automated Mode (Harness Integration)

当被 `ai-drama-harness` 调用时，除了正常的 markdown 输出，**额外输出一个结构化 JSON 代码块**，供 harness 通过 `python cli.py write --table 剧本设定` 写入飞书。

### 读取输入

无需读取（本 skill 是流程起点）。

### JSON 输出格式

在 markdown 输出末尾，附加以下代码块：

````
```json:structured-output
[
  {"name": "剧名", "value": "...", "global_prompt": ""},
  {"name": "一句话卖点", "value": "...", "global_prompt": ""},
  {"name": "题材类型", "value": "...", "global_prompt": ""},
  {"name": "基调", "value": "...", "global_prompt": ""},
  {"name": "剧情简介", "value": "...", "global_prompt": ""},
  {"name": "世界观规则", "value": "...", "global_prompt": ""},
  {"name": "主线与冲突", "value": "...", "global_prompt": ""},
  {"name": "画面风格", "value": "...", "global_prompt": "画风描述，供全局继承"},
  {"name": "平台调性", "value": "竖屏短剧9:16", "global_prompt": ""},
  {"name": "剧本节奏", "value": "...", "global_prompt": ""},
  {"name": "剧本看点", "value": "...", "global_prompt": ""},
  {"name": "主要角色清单", "value": "角色1、角色2、...", "global_prompt": ""},
  {"name": "全集大纲", "value": "第1集：...；第2集：..."}
]
```
````

**注意**：`画面风格` 的 `global_prompt` 字段会被三视图、场景等 skill 继承为画风前缀。
