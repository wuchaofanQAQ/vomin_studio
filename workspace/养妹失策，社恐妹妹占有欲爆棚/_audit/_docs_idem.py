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
("3. **轻量确认**（不计为正式确认点）：展示资产清单表（类型/名称/新建或复用/描述字数）与写入清单，确认后写入文字资产（不出图）：",
 "3. **轻量确认**（不计为正式确认点）：展示资产清单表（类型/名称/新建或复用/描述字数）与写入清单，确认后写入文字资产（不出图）。**只写新建项**；复用项不进 data（写入按 `name` upsert，`status=复用` 的行 CLI 也会跳过）："),
("   python skills/script-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json",
 "   python skills/script-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json --library $WS"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("规则：\n\n- **只写描述（≤50 字）**，不写提示词、不写空间锚点、不写角色档案/音色；由 `check_assets.py` 卡死。\n- 复用项不重写描述。",
 "规则：\n\n- **只写描述（≤50 字）**，不写提示词、不写空间锚点、不写角色档案/音色；由 `check_assets.py` 卡死。\n- **幂等**：每次先读角色库；同名（归一化后）标 `复用`，不写进 payload。写入按 `name` upsert，同名不会新增行。"),
("### 场景引用语法",
 "### 幂等\n\n每次先读场景库；同名（归一化后：去空格、半角括号统一）标 `复用`，不写进 payload。写入按 `场景ID` upsert，同名不会新增行；`status=复用` 的行 CLI 会跳过。\n\n### 场景引用语法"),
])
print("done")
