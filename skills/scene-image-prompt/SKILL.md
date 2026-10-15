---
name: scene-image-prompt
description: 根据剧本设定/分集场景描述，生成可直接用于豆包 seedream 文生图的"场景空镜图"AIGC 提示词。场景规格固定：单张、16:9 横版、纯空镜无角色、主体占画面约 3/4 留 1/4、明确前/中/后三层景深。当用户需要"场景图""场景空镜""场景背景""场景 prompt""背景图提示词"，或要把分集剧本里的场景描述转成能出场景图的 prompt 时使用。本 skill 只产出提示词，不调用出图工具。
---

# Scene Image Prompt

## Overview

把剧本设定 + 分集里的场景描述，转成**一条可直接投喂豆包 seedream** 的场景空镜图提示词。与角色 skill 不同，场景是**单张 16:9 横版、纯空镜、无角色**，专为"后续把角色/人物叠加进去"预留空间。

## 场景 vs 角色 规格对比

| 维度 | 场景图 | 角色图（character-three-view）|
|---|---|---|
| 张数 | 单张 | 4 张 |
| 比例 | **16:9 横版** | 9:16 竖版 |
| 内容 | 纯空镜无角色 | 角色全身/人头 |
| 构图 | 主体占 3/4 + 前中后三层景深 | 人物居中 |
| 用途 | 做背景，后续叠加角色 | 角色一致性资产 |

## Workflow

### Step 1 — 抽取场景要素

从剧本设定 + 分集场景描述中抽取：

1. **场景类型**：室内/室外、具体地点（办公室/废墟/古战场…）
2. **时代/风格**：从剧本设定继承
3. **主体物**：场景中心主体（建筑/山/街道/装置…）
4. **环境氛围**：光线（日/夜/黄昏）、天气、色调
5. **层次要素**：前景/中景/背景分别是什么（用于三层景深）

缺失项标"未指定"，不臆造。

### Step 2 — 组装场景提示词

用 `references/prompt-blueprint.md` 模板，按固定段落顺序组装单条 prompt。核心规则：

- **16:9 横版**、单张、纯空镜无角色
- **主体占画面约 3/4，留出约 1/4 空间**（为角色植入留位）
- **前/中/后三层景深明确**，让 AI 理解场景空间层次
- **无人物、无文字**；如需画面有文字用中文引号标注
- 画风从剧本设定继承（`references/scene-lexicon.md`）

### Step 3 — 输出与说明

输出提示词，附 2–3 行说明：场景类型、主体与三层景深如何确定、哪些项未指定。用户修正 → 更新对应段落重出整条 prompt。

## References

- `references/prompt-blueprint.md` — 场景提示词分段模板与完整示例（必读）
- `references/scene-lexicon.md` — 场景类型/氛围词表 + 三层景深写法

## Automated Mode (Harness Integration)

当被 `ai-drama-harness` 调用时，额外输出结构化 JSON，供 harness 通过 `python cli.py write --table 场景库` 写入飞书。

### 读取输入

```bash
python cli.py read $WS --table 剧本设定
```

### JSON 输出格式

````
```json:structured-output
[
  {
    "name": "写字楼大堂",
    "description": "现代化写字楼一层大堂，大理石地面...",
    "gen_prompt": "16:9横构图，现代写字楼大堂，大理石地面...",
    "source": "AIGC生成"
  }
]
```
````

harness 写入后通过 `python cli.py generate $WS --target 场景库:写字楼大堂` 触发出图。
