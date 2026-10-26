# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:30]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\SKILL.md", [
("### A2: 角色三视图 → 出图", "### A2: 角色资产图 → 出图"),
("1. 调用 `character-three-view-prompt` skill，为每个核心角色出三视图提示词（草案）",
 "1. 调用 `asset-image-generation` skill，为每个核心角色写四视角设定图提示词（草案）"),
("5. 资产图**懒加载出图**：待 B1 确定本集 `dependencies` 后，只为本集用到的资产生成（花预算，清单须列对象与预估花费）。场景图出完须过 `script-asset-extraction/references/scene-consistency.md` 的**一致性检查**，硬指标不过不得进入视频生成。要出「场景资料板」（左大正视图 + 右侧东南西北四视角、22:9）时改用 `scene-board-image` skill，默认只出 1 张",
 "5. 资产图**懒加载出图**：待 B1 确定本集 `dependencies` 后，调用 `asset-image-generation` 按类型套版式（角色四视角 / 场景四视角资料图 / 道具双视角），只为本集用到的资产生成（花预算，清单须列对象与预估花费）。逐张过验收清单；场景图出完还须过 `script-asset-extraction/references/scene-consistency.md` 的**一致性检查**，硬指标不过不得进入视频生成"),
("| `character-three-view-prompt` | A2 | 角色 → 三视图出图提示词 |",
 "| `asset-image-generation` | A2/B0b | 角色/场景/道具 → 版式化提示词 + 出图 + 逐张验收 |"),
("| `scene-board-image` | B0b | 单个场景 → 场景资料板提示词（左大正视图+右侧东南西北四视角，22:9）+ 出图 |\n", ""),
])

rep(r"skills\ai-drama-harness\references\pipeline.md", [
("| ② | character-three-view-prompt | 角色档案+画风 | 三视图出图提示词（可选，主角用） | `read --table 角色库` | `write --table 角色库`（gen_prompt）+ `generate` |",
 "| ② | asset-image-generation | 角色库描述+画风 | 角色四视角提示词 + 出图（可选，主角用） | `read --table 角色库` | `write --table 角色库`（gen_prompt）+ `generate` |"),
("                 ├→ ② character-three-view-prompt（主角三视图，可选）→ generate ──(确认点2·飞书)",
 "                 ├→ ② asset-image-generation（主角四视角设定图，可选）→ generate ──(确认点2·飞书)"),
("A2: ② character-three-view-prompt 产出提示词草案（可选）",
 "A2: ② asset-image-generation 产出角色提示词草案（可选）"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("## 2. 角色三视图提示词（character-three-view-prompt → 角色库 gen_prompt）",
 "## 2. 角色资产图提示词（asset-image-generation → 角色库 gen_prompt）"),
("```json\n[\n  {\"name\": \"林砚\", \"gen_prompt\": \"正面全身照，28岁亚洲男性...\"}\n]\n```",
 "固定四视角版式，由 `asset_prompt.py build --type 角色 --desc 描述` 生成：\n\n```text\n角色四视角设定图，同一角色，四格布局：画面上三分之一，左侧为人物近景正视图，右侧为人物近景侧视图；画面下三分之二，左侧为人物全身正视图，右侧为人物全身背视图。浅净背景，画面内无任何文字。真人电影级写实质感，保留真实皮肤纹理与自然光影；四视角为同一人，五官、发型、服装、体型完全一致。\n角色外观：{描述}\n```\n\n16:9；`generate` 出图后回填 `文件路径`。场景/道具同理由同一 skill 出图（场景 22:9 四视角资料图、道具 16:9 双视角）。"),
("| B 风格 | `style_desc` | character-three-view-prompt |",
 "| B 风格 | `style_desc` | asset-image-generation |"),
("| D 外貌 | `appearance` | character-three-view-prompt、script-to-prompt-30 |",
 "| D 外貌 | `appearance` | asset-image-generation、script-to-prompt-30 |"),
])

rep(r"CLAUDE.md", [
("| character-three-view-prompt | `skills/character-three-view-prompt/SKILL.md` | 出角色三视图 |",
 "| asset-image-generation | `skills/asset-image-generation/SKILL.md` | 出角色四视角、场景四视角资料图、道具双视角 |"),
("| scene-board-image | `skills/scene-board-image/SKILL.md` | 场景资料板、场景图资料板、生成场景板、出场景图 |\n", ""),
])

rep(r"skills\AI短剧生产底座使用手册.md", [
("  → ② character-three-view-prompt 角色三视图提示词          → 触发出图",
 "  → ② asset-image-generation 角色/场景/道具版式化出图        → 触发出图"),
("| 出角色三视图 | \"出角色三视图 / 角色4张照片提示词\" | character-three-view-prompt |",
 "| 资产生图 | \"出角色图 / 三视图 / 场景资料板 / 出道具图 / 四视角\" | asset-image-generation |"),
])

rep(r"skills\drama-initializer\SKILL.md", [
("产出后下游衔接：角色三视图（character-three-view-prompt）、逐集小说转剧本（novel-to-script）、场景抽取（script-asset-extraction）、分镜与提示词（script-to-prompt-30）。",
 "产出后下游衔接：资产提取（script-asset-extraction）、资产生图（asset-image-generation）、逐集小说转剧本（novel-to-script）、分镜与提示词（script-to-prompt-30）。"),
("- 角色三视图/定妆照 → `character-three-view-prompt`（吃角色库 appearance + 画面风格）",
 "- 角色资产图/四视角 → `asset-image-generation`（吃角色库描述 + 画面风格）"),
])

rep(r"skills\drama-initializer\references\setting-template.md", [
("> 此节直接喂给 `character-three-view-prompt` 和 `script-asset-extraction` 的画风词表，务必写清。",
 "> 此节直接喂给 `asset-image-generation` 和 `script-asset-extraction` 的画风词表，务必写清。"),
])

rep(r"skills\drama-initializer\references\character-extract-init.md", [
("- 角色库**不写** `gen_prompt`（三视图提示词由 `character-three-view-prompt` 生成）",
 "- 角色库**不写** `gen_prompt`（资产图提示词由 `asset-image-generation` 生成）"),
])
print("done")
