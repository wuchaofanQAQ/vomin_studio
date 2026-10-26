# -*- coding: utf-8 -*-
import re, os
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()

# 删掉 p01 镜头12 末尾那句残缺 OS（完整版在 p02 开头）
old = "[26.5s-30s]，【陈诚】（OS、放得很低说）：「十二岁生日那天，蛋糕的味道涌上来。」\n"
assert t.count(old) == 1, t.count(old)
t = t.replace(old, "")
open(p, "w", encoding="utf-8").write(t)
print("removed truncated OS from p01 shot12")

# 模糊查重：一句是另一句的前缀且≥8字
pat = re.compile(r"^\[[\d.]+s-[\d.]+s\]\uff0c(.+?)\uff1a\u300c(.+)\u300d$")
lines = []
for ln in t.splitlines():
    m = pat.match(ln.strip())
    if m:
        lines.append((m.group(2), ln.strip()[:30]))
dups = []
for i, (a, la) in enumerate(lines):
    for j, (b, lb) in enumerate(lines):
        if i != j and len(a) >= 8 and b.startswith(a):
            dups.append((la, lb))
print("prefix-dups:", len(dups))
for d in dups[:5]:
    print(" ", d[0], "->", d[1])
