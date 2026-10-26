# -*- coding: utf-8 -*-
import re
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
n = len(re.findall(r"【([^】]+)】\1", t))
t = re.sub(r"【([^】]+)】\1", r"【\1】", t)
open(p, "w", encoding="utf-8").write(t)
print("deduped", n)
print([l for l in t.splitlines() if l.startswith("【参考图映射】")][0][:120])
