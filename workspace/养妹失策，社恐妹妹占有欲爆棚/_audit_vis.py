# -*- coding: utf-8 -*-
import re, os
base = r"__WS__"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
segs = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5.*?\u3011)\s*$", md)
SIZE = ["大特写","特写","中近景","近景","中景","全景","远景"]
LAYER = ["前景","中景","后景","画左","画右","画面","入画","反射","影子","虚化"]
print("镜 | 景别 | 主体 | 其他角色提及 | 有无位置词 | 原句")
for i in range(1, len(segs), 2):
    sno = re.match(r"\u3010\u7b2c(\d+)\u6bb5", segs[i]).group(1)
    body = segs[i+1]
    for m in re.finditer(r"(?ms)^\u3010\u955c\u5934(\d+)\uff5c\[([\d.]+)s-([\d.]+)s\]\uff5c(.+?)\u3011\n(.*?)(?=\n\u3010|\Z)", body):
        no, a, b, title, txt = m.groups()
        first = re.search(r"\u3010([^\u3011]+)\u3011", txt)
        subj = first.group(1) if first else "-"
        others = [x for x in re.findall(r"\u3010([^\u3011]+)\u3011", txt) if x != subj]
        size = next((s for s in SIZE if s in txt[:40]), "?")
        if not others: continue
        # 只关心 近景/特写 里出现的其他角色
        if size not in ("近景","特写","大特写"): continue
        for o in set(others):
            pos = [l for l in LAYER if l in txt]
            idx = txt.find("【"+o+"】")
            ctx = txt[max(0,idx-16):idx+len(o)+10].replace("\n"," ")
            print(f"{sno}/{no} | {size} | {subj} | {o} | {'有' if any(l in ctx for l in LAYER) else '无'} | {ctx}")
