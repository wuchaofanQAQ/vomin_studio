# -*- coding: utf-8 -*-
import re
md = open(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md", encoding="utf-8").read()
print("过肩:", md.count("过肩"), "| 俯拍:", md.count("俯拍"), "| 起幅:", md.count("起幅"), "| 落幅:", md.count("落幅"))
two = [l[:50] for l in md.splitlines() if l.startswith("硬切") and ("近景" in l[:14] or "特写" in l[:14]) and len(re.findall("【", l)) > 2]
print("近景/特写里含 3 个以上【】的镜头:", len(two))
for x in two:
    print("  ", x)
