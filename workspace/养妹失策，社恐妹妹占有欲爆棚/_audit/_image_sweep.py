# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:26]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\SKILL.md", [
("| 2 | 角色形象 | A2 | 飞书审核 | 三视图 generate |",
 "| 2 | 角色形象 | A2 | 飞书审核 | 四视角 generate |"),
("- 新增角色 → 走角色档案 + 三视图补生成",
 "- 新增角色 → 走 `asset-image-generation` 补四视角设定图"),
("| `script-asset-extraction` | B0b | 剧本+小说 → 角色/场景/道具资产（文字描述 + ≤50 字提示词）+ 角色档案 + 场景锚点 |",
 "| `script-asset-extraction` | B0b | 剧本+小说 → 角色/场景/道具资产（一句 ≤50 字描述） |"),
])

rep(r"skills\ai-drama-harness\references\checkpoint-protocol.md", [
("| 2 | 角色形象 | A2 | 飞书审核 | 写 gen_prompt + generate 角色三视图 |",
 "| 2 | 角色形象 | A2 | 飞书审核 | 写 gen_prompt + generate 角色四视角 |"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("下游消费：角色三视图、script-asset-extraction（画风/画幅）、script-to-prompt-30（世界观/节奏/看点）。",
 "下游消费：asset-image-generation（画风/画幅）、script-asset-extraction、script-to-prompt-30（世界观/节奏/看点）。"),
("- `new_characters` → 调对应 skill 补角色档案 + 三视图",
 "- `new_characters` → 回 `script-asset-extraction` 补描述，再用 `asset-image-generation` 出四视角"),
("3. **画风全局继承**：三视图、场景、视频提示词的画风一律取剧本设定 `画面风格`",
 "3. **画风全局继承**：角色/场景/道具资产图、视频提示词的画风一律取剧本设定 `画面风格`"),
])

rep(r"skills\ai-drama-harness\references\pipeline.md", [
("| ④ | script-asset-extraction（逐集 B0b） | 当前集±1集 script + 当前集小说原文（`--with-novel`）+ 剧本设定 + 角色库/角色档案/场景库/道具库 | 角色/场景/道具资产：文字描述 + 提示词（≤50 字）+ 角色档案 + 场景锚点 + 复用/待补清单 | `read --table 剧本表 --episode N --context 1` + `--episode N --with-novel` + 四张资产表 | `write --table 角色库/角色档案/场景库/道具库` + `generate`（懒加载） |",
 "| ④ | script-asset-extraction（逐集 B0b） | 当前集±1集 script + 当前集小说原文（`--with-novel`）+ 剧本设定 + 角色库/场景库/道具库 | 角色/场景/道具资产：一句 ≤50 字描述 + 复用/待补清单 | `read --table 剧本表 --episode N --context 1` + `--episode N --with-novel` + 三张资产表 | `write --table 角色库/场景库/道具库` + `generate`（懒加载） |"),
("- 角色、场景、道具由 ④ 一个技能统一提取，**每个资产一行一张图**，产出「文字描述 + ≤50 字提示词」。",
 "- 角色、场景、道具由 ④ 一个技能统一提取，**每个资产一行一张图**，只产一句 ≤50 字描述。"),
("    read 剧本设定 + 角色库 + 角色档案 + 场景库 + 道具库\n    → 角色/场景/道具清单：描述 + ≤50 字提示词 + 复用判定 + 场景锚点",
 "    read 剧本设定 + 角色库 + 场景库 + 道具库\n    → 角色/场景/道具清单：一句描述 + 复用判定"),
("**调用权在 script-to-prompt-30（B1）**：依据场景锚点设计站位与调度，产出本集 `dependencies`（scenes / characters / props），作为懒加载依据。",
 "**调用权在 script-to-prompt-30（B1）**：依据场景描述设计站位与调度，产出本集 `dependencies`（scenes / characters / props），作为懒加载依据。"),
])

rep(r"skills\AI短剧生产底座使用手册.md", [
("→ ④ script-asset-extraction   剧本+小说 → 角色/场景/道具资产（≤50 字描述 + 角色档案 + 场景锚点）",
 "→ ④ script-asset-extraction   剧本+小说 → 角色/场景/道具资产（一句 ≤50 字描述）"),
("├→ ② 角色三视图（吃角色档案+画风）→ generate 出图",
 "├→ ② 资产图（角色四视角 / 场景四视角资料图 / 道具双视角）→ generate 出图"),
("6. **画风全局继承**：三视图、场景、视频提示词的画风一律取剧本设定",
 "6. **画风全局继承**：资产图、视频提示词的画风一律取剧本设定"),
("7. **一致性锚点**：角色三视图是后续所有画面的人脸标准",
 "7. **一致性基准**：角色四视角设定图是后续所有画面的人脸标准"),
("| B 风格层 | 画风/主色调/气质 | `style_desc` | 三视图、视频 |",
 "| B 风格层 | 画风/主色调/气质 | `style_desc` | 资产图、视频 |"),
("| D 外貌层 | 年龄/脸型/五官/发型/身体/服装/标志特征 | `appearance` | 三视图出图 |",
 "| D 外貌层 | 年龄/脸型/五官/发型/身体/服装/标志特征 | `appearance` | 资产图出图 |"),
])
print("done")
