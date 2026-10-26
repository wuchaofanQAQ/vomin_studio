# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '"跟摇", "环绕", "焦点转移", "上摇", "下摇", "摇镜", "俯拍", "仰拍", "航拍", "手持"]'
new = ('"跟摇", "环绕", "焦点转移", "上摇", "下摇", "摇镜", "俯拍", "仰拍", "航拍", "手持",\n'
       '          "机位", "过肩", "主观", "反打", "贴地", "低机位", "高机位"]')
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("checker 机位词已扩")
