# -*- coding: utf-8 -*-
import re, os
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
assert "十四镜按下列时码" in t
t = t.replace("十四镜按下列时码", "十二镜按下列时码")

# 全片镜数声明核对
segs = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5.*?\u3011)\s*$", t)
for i in range(1, len(segs), 2):
    head, body = segs[i], segs[i + 1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    m = re.search(r"([一二三四五六七八九十]+)镜按下列时码", body)
    cn = m.group(1) if m else "?"
    print(head[:14], "实际", n, "声明", cn)
open(p, "w", encoding="utf-8").write(t)
print("fixed p01 count")
