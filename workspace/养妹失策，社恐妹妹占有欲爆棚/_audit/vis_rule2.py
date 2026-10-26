# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'if size not in ("近景", "特写", "大特写"):'
new = 'if size not in ("近景", "中近景", "特写", "大特写"):'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("extended to 中近景")
