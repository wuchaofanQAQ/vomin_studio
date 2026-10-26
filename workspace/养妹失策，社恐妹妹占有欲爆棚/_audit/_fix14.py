# -*- coding: utf-8 -*-
import re, os
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'LOCK_RE = re.compile(r"^【([^】]+)】\\s*(?:画面参考\\s*[:：])?\\s*\\{([^：}]+)[:：]([^}]+)\\}")'
new = 'LOCK_RE = re.compile(r"^【([^】]+)】\\s*(?:画面参考\\s*[:：])?\\s*[:：]?\\s*\\{([^：}]+)[:：]([^}]+)\\}")'
assert t.count(old) == 1, "LOCK_RE not found"
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("LOCK_RE fixed")

p2 = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
s = open(p2, encoding="utf-8").read()
out = []
for ln in s.splitlines():
    if ln.startswith("## 【第") or ln.startswith("【镜头"):
        for a in ("【陈诚公寓玄关】", "【陈诚公寓走廊】", "【沈幼怡】", "【陈诚】", "【行李箱】", "【双肩书包】"):
            ln = ln.replace(a, a.strip("【】"))
    out.append(ln)
open(p2, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("headers unwrapped")
