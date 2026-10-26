# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'IMG_TABLES = {"场景库", "角色库", "道具库", "素材库"}'
new = 'IMG_TABLES = {"场景库", "角色库", "道具库", "素材库", "资产库"}'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("checker updated")
