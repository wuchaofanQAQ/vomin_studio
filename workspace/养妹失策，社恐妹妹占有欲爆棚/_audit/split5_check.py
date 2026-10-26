# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 拆出所有镜头（保留正文与台词）
shots = re.findall(r"(?ms)^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.*?)(?=^【镜头|\n## |\Z)", s)
cur = [(int(n), t, b.strip()) for n, t, b in shots]
print("total shots:", len(cur))

def block(no, dur, title):
    return f"## 【第{no:02d}段｜[0s-{dur}s]｜{title}】\n\n"

def shot(n, a, b, title, body):
    return f"【镜头{n:02d}｜[{a:g}s-{b:g}s]｜{title}】\n{body}\n\n"

# S1 = 原 p01 前 14 镜；S2 = 原 p02 13 镜；S3 = 原 p03 前 4 镜；S4 = 原 p03 后 7 镜 + 原 p04 前 3 镜；S5 = 原 p04 后 9 镜
s1, s2 = cur[0:14], cur[14:27]
s3 = cur[27:31]
s4 = cur[31:38] + cur[38:41]
s5 = cur[41:50]
print(len(s1), len(s2), len(s3), len(s4), len(s5))
