# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '"机位", "过肩", "主观", "反打", "贴地", "低机位", "高机位"]'
new = '"机位", "过肩", "主观", "反打", "贴地", "低机位", "高机位",\n          "门内", "门外", "室内", "窗外", "视角", "机位侧"]'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("已补空间机位词")
