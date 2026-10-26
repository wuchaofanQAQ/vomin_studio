# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
lines = open(f, encoding="utf-8").read().split("\n")
out, cur = [], None
for ln in lines:
    m = re.match(r"^【镜头\d+｜\[([\d.]+)s-([\d.]+)s\]｜", ln)
    if m:
        cur = (m.group(1), m.group(2)); out.append(ln); continue
    m2 = re.match(r"^\[[\d.]+s-[\d.]+s\](.*)$", ln)
    if m2 and cur:
        out.append(f"[{cur[0]}s-{cur[1]}s]{m2.group(1)}"); continue
    out.append(ln)
s = "\n".join(out)
# 每段末镜收口到段长
parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-([\d.]+)s\]｜.*?】)$", s)
res = [parts[0]]
i = 1
while i < len(parts):
    head, dur, body = parts[i], float(parts[i+1]), parts[i+2]
    ms = list(re.finditer(r"【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]", body))
    if ms:
        last = ms[-1]
        if abs(float(last.group(3)) - dur) > 0.05:
            body = body.replace(last.group(0), f"【镜头{int(last.group(1)):02d}｜[{last.group(2)}s-{dur:g}s]", 1)
            body = re.sub(r"\[[\d.]+s-[\d.]+s\]，", f"[{last.group(2)}s-{dur:g}s]，", body)
    res += [head, body]
    i += 3
open(f, "w", encoding="utf-8").write("".join(res))
print("台词窗口对齐 + 段尾收口")
