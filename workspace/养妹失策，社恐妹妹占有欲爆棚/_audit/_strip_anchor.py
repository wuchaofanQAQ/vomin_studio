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
("   - **角色**（含群像）：一句文字描述（≤50 字）+ 6 模块档案（新角色）",
 "   - **角色**（含群像）：一句文字描述（≤50 字）"),
("   - **场景**：一场景一图，一句描述（≤50 字）+ 空间锚点",
 "   - **场景**：一场景一图，一句描述（≤50 字）"),
("   python cli.py write $WS --table 角色库   --data @characters.json\n   python cli.py write $WS --table 角色档案 --data @bibles.json\n   python cli.py write $WS --table 场景库   --data @scenes.json\n   python cli.py write $WS --table 道具库   --data @props.json",
 "   python cli.py write $WS --table 角色库 --data @characters.json\n   python cli.py write $WS --table 场景库 --data @scenes.json\n   python cli.py write $WS --table 道具库 --data @props.json"),
("场景图出完须过 `script-asset-extraction/references/scene-anchors.md` 的**一致性检查**",
 "场景图出完须过 `script-asset-extraction/references/scene-consistency.md` 的**一致性检查**"),
])

rep(r"skills\ai-drama-harness\references\pipeline.md", [
("每个资产给文字描述与 ≤50 字提示词；场景写空间锚点。逐集增量：同名同图复用。",
 "每个资产给一句 ≤50 字描述（不写提示词、锚点、档案）。逐集增量：同名同图复用。"),
("场景图出完过 `script-asset-extraction/references/scene-anchors.md` 的一致性检查",
 "场景图出完过 `script-asset-extraction/references/scene-consistency.md` 的一致性检查"),
])

rep(r"skills\AI短剧生产底座使用手册.md", [
("每个资产给一句 ≤50 字描述（场景另带空间锚点），新角色另产 6 模块档案；无小说原文时只用剧本，库里已有的资产直接复用。",
 "每个资产给一句 ≤50 字描述；无小说原文时只用剧本，库里已有的资产直接复用。"),
("读本集剧本 + 小说原文 → 角色/场景/道具清单（≤50 字描述 + 空间锚点 + 角色档案）",
 "读本集剧本 + 小说原文 → 角色/场景/道具清单（≤50 字描述）"),
])

rep(r"skills\script-to-prompt-30\SKILL.md", [
("- **一段尽量只用一个场景**：跨场景会让场景图和空间锚点翻倍，优先在场景交界处断开。",
 "- **一段尽量只用一个场景**：跨场景会让场景图数量翻倍，优先在场景交界处断开。"),
])

rep(r"skills\script-asset-extraction\references\asset-rules.md", [
("- **不出现的不建**：只被提到、没有出镜的角色，不进角色库；如果台词需要声音，走 `角色档案` 的音色，不需要图。",
 "- **不出现的不建**：只被提到、没有出镜的角色，不进角色库（台词需要声音时由 `角色档案` 的音色负责，不需要图）。"),
])
print("done")
