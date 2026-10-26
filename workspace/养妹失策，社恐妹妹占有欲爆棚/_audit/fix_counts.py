# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()
CN = {9:"九",11:"十一",12:"十二",13:"十三",14:"十四",15:"十五",16:"十六",17:"十七"}

parts = re.split(r"(?m)^(## 【第\d+段.*?】)$", t)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{CN.get(n, n)}镜按下列时码", body, count=1)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("镜数声明已修正")
