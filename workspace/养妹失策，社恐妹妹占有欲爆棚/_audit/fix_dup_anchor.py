# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "场景/角色**必须**带 `{资产库：名}` / `{资产库：名}`；道具**有参考图时**带 `{资产库：名}`"
new = "场景/角色**必须**带 `{资产库：名}`；道具**有参考图时**带 `{资产库：名}`"
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "| 素材锚点 | `{资产库：名}` / `{资产库：名}` / `{资产库：名}` 写在资产锁定条目里"
new2 = "| 素材锚点 | `{资产库：名}` 写在资产锁定条目里"
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("fixed duplicate anchors")
