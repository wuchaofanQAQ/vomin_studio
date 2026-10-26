# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-extraction\SKILL.md"
t = open(p, encoding="utf-8").read()
anchor = "6. **不改剧情**"
add = "7. **关联集数只填已有剧本的集**：只有「剧本表里已有剧本、且本资产真的用到」的集号才写；没用到、或剧本还没写的集，**留空**，不预填未来集数（如 `2,3`）。\n\n"
assert t.count(anchor) == 1
t = t.replace(anchor, add + anchor)
open(p, "w", encoding="utf-8").write(t)
print("skill 已加第 7 条铁律")
