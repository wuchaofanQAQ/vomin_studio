# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:24]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\SKILL.md", [
("B0a 写入剧本表之后、拆分镜之前运行。**逐集增量**：库里已有的资产直接复用，只为新资产补描述与提示词；一个资产 = 一行 = 一张图。",
 "B0a 写入剧本表之后、拆分镜之前运行。**逐集增量**：库里已有的资产直接复用，只为新资产补一句描述；一个资产 = 一行 = 一张图。"),
("   python cli.py read $WS --table 角色库\n   python cli.py read $WS --table 角色档案\n   python cli.py read $WS --table 场景库",
 "   python cli.py read $WS --table 角色库\n   python cli.py read $WS --table 场景库"),
])

rep(r"skills\scene-board-image\SKILL.md", [
("- **场景内容**取该场景的 `场景描述`（含【空间锚点】【光源】【物件清单】等段）；缺项按「真实可拍」补全，不新增剧情",
 "- **场景内容**取该场景的 `场景描述`（空间/材质/光线）；描述不够时按「真实可拍」补全，不新增剧情"),
])
print("done")
