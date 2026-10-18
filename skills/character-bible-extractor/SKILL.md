---
name: character-bible-extractor
description: 从剧本设定 + 分集内容中，抽取并生成每个角色的结构化"角色档案/角色圣经"（Character Bible）。当用户需要"角色档案""角色设定卡""角色人设卡""从剧本里提取角色""建立角色一致性档案"，或要为短剧角色建立统一标准供后续出图/分镜使用时使用。本 skill 产出结构化角色档案文档，不直接出图。
---

# Character Bible Extractor

## Overview

把"剧本设定（全局画风）+ 各集出现的角色段落"加工成**每个角色一份的结构化档案**。这份档案是角色一致性的唯一标准源，供 `character-three-view-prompt`（出图）、分镜、场景等所有下游 skill 复用。

## Workflow

### Step 1 — 锁定输入

- 读取**剧本设定**（全局画风/世界观）
- 从分集内容中，按角色抽取**该角色出现的段落**（不读与角色无关的全集全文，控制体积）

### Step 2 — 逐角色抽取要素

对每个角色，按 `references/bible-template.md` 的 14 项要素抽取。关键规则：

- 缺失项标"未指定"，**不臆造**（不替编剧脑补设定）
- **标志性特征**（伤疤/纹身/道具/独特穿着）是后续出图一致性的锚点，必须完整保留
- **画风基调**从剧本设定继承，写入档案（供三视图 skill 使用）
- 从各集跨集汇总，避免"只看某一集导致人设漂移"

### Step 3 — 输出角色档案

每角色一份档案（`references/bible-template.md` 8 模块模板）。标注：
- 角色名 / 定位（主角/反派/配角）
- 出场集数范围
- 从哪几集抽取

8 模块：基本信息(A)、风格(B)、音色(C)、外貌(D)、性格(E)、战斗(F)、标志性表达(G)、标注(H)。B/C/F/G 是新增的短剧专用字段，缺失标"未指定"，不臆造。

### Step 4 — 交接

档案末尾标注下游用途：
- 外貌(D)+风格(B) → `character-three-view-prompt`
- 性格(E)+台词(G) → `storyboard-prompt`（分镜演出与角色台词）
- 战斗(F)+特效(F) → `storyboard-prompt`（打斗镜头/特效描写）、视频生成
- 音色(C) → 配音/TTS

> 注：`drama-initializer` 剧本初始化时已产出角色档案初版；本技能用于在其基础上补全/深化 8 模块。

## References

- `references/bible-template.md` — 角色档案字段模板（必读，逐字段对照）
- `references/role-extraction.md` — 跨集抽取规则与去漂移检查清单

## Automated Mode (Harness Integration)

当被 `ai-drama-harness` 调用时，额外输出结构化 JSON，供 harness 分别写入角色库和角色档案两张表。

### 读取输入

```bash
python cli.py read $WS --table 剧本设定
```

### JSON 输出格式

产出**双表 JSON**，harness 拆分后分别写入角色库（精简版：供生图/TTS）和角色档案（完整 8 模块：供编剧/分镜/战斗）。

````
```json:structured-output
{
  "角色库": [
    {
      "name": "林砚",
      "char_type": "核心",
      "appearance": "28岁亚洲男性，方脸，黑色短发...",
      "voice_desc": "青年男，沉稳低沉，语速中等",
      "source": "AIGC生成"
    }
  ],
  "角色档案": [
    {
      "name": "林砚",
      "char_type": "核心",
      "basic_info": "角色名：林砚\n定位：主角\n出场集数：第1-30集\n身份：...",
      "style_desc": "画风基调：电影级写实\n主色调倾向：冷蓝灰\n整体气质：冷峻",
      "voice_desc": "青年男，沉稳低沉，语速中等",
      "appearance": "脸型：方脸\n头发：黑色短发\n五官：...[完整D模块]",
      "personality": "性格：内敛冷静\n动机：...\n说话风格：...[完整E模块]",
      "battle_desc": "战斗风格：近身格斗\n招式：...[完整F模块，缺失标'未指定']",
      "signature_expr": "经典动作：...\n口头禅：...[完整G模块]",
      "notes": "来源集数：第1-5集\n缺失项：战斗招式未指定..."
    }
  ]
}
```
````

harness 提取 JSON 后按表名 key 拆分写入：
```bash
python cli.py write $WS --table 角色库 --data '<角色库部分>'
python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
```
