# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()
parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-(\d+)s\]｜.*?】)$", t)
out, i = [parts[0]], 1
while i < len(parts):
    head, dur, body = parts[i], int(parts[i+1]), parts[i+2]
    ms = list(re.finditer(r"【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]", body))
    if ms:
        last = ms[-1]
        a1, b1 = last.group(2), last.group(3)
        body = body.replace(f"[{a1}s-{b1}s]｜", f"[{a1}s-{dur}s]｜", 1)
        body = body.replace(f"[{a1}s-{b1}s]，", f"[{a1}s-{dur}s]，", 1)
    out += [head, body]
    i += 3
open(f, "w", encoding="utf-8").write("".join(out))
print("段尾收口完成")
