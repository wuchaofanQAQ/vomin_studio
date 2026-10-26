# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '"门内", "门外", "室内", "窗外", "视角", "机位侧"]'
new = '"门内", "门外", "室内", "窗外", "视角", "机位侧",\n          "眼平齐", "齐高", "侧前方", "侧后方", "贴屏幕", "贴近", "平视"]'
assert t.count(old) == 1
t = t.replace(old, new)
t = t.replace("head = body[:80]", "head = body[:110]")
open(p, "w", encoding="utf-8").write(t)
print("checker 窗口 80→110，补位置词")
