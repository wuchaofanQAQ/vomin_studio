# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep02_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
segs = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
print("段 | 镜头 | 时长 | 每镜平均")
for i in range(1, len(segs), 2):
    head, body = segs[i], segs[i+1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    dur = float(re.search(r"\[0s-([\d.]+)s\]", head).group(1))
    print(f"{head[2:6]} | {n:2d} | {dur:.0f}s | {dur/n:.2f}s")
# 裸名/重复台词的粗查
lines = re.findall(r"^\[[\d.]+s-[\d.]+s\]，(.*?)：(.*)$", s, re.M)
texts = [t for _, t in lines]
print("台词行:", len(texts), "| 重复:", len([t for t in set(texts) if texts.count(t) > 1]))
