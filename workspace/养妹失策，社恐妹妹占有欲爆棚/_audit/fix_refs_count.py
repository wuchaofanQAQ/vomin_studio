# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'refs = [len(s["map"]) for s in segs]'
new = 'refs = [len(s["map"]) or len([e for e in s["lock"] if e["table"] in IMG_TABLES]) for s in segs]'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("refs 计算已修")
