# -*- coding: utf-8 -*-
import re, os, sys
base = sys.argv[1]
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
segs = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5.*?\u3011)\s*$", md)
SIZE = ["\u5927\u7279\u5199", "\u7279\u5199", "\u4e2d\u8fd1\u666f", "\u8fd1\u666f", "\u4e2d\u666f", "\u5168\u666f", "\u8fdc\u666f"]
LAYER = ["\u524d\u666f", "\u4e2d\u666f", "\u540e\u666f", "\u753b\u5de6", "\u753b\u53f3", "\u753b\u9762", "\u5165\u753b", "\u53cd\u5c04", "\u5f71\u5b50", "\u865a\u5316"]
print("seg/shot | size | subject | other | has_position | sentence")
for i in range(1, len(segs), 2):
    m0 = re.match(r"\u3010\u7b2c(\d+)\u6bb5", segs[i])
    sno = m0.group(1)
    body = segs[i + 1]
    for m in re.finditer(r"(?ms)^\u3010\u955c\u5934(\d+)\uff5c\[([\d.]+)s-([\d.]+)s\]\uff5c(.+?)\u3011\n(.*?)(?=\n\u3010|\Z)", body):
        no, a, b, title, txt = m.groups()
        first = re.search(r"\u3010([^\u3011]+)\u3011", txt)
        subj = first.group(1) if first else "-"
        others = [x for x in re.findall(r"\u3010([^\u3011]+)\u3011", txt) if x != subj]
        size = next((s for s in SIZE if s in txt[:40]), "?")
        if not others or size not in ("\u8fd1\u666f", "\u7279\u5199", "\u5927\u7279\u5199"):
            continue
        for o in dict.fromkeys(others):
            idx = txt.find("\u3010" + o + "\u3011")
            ctx = txt[max(0, idx - 18):idx + len(o) + 12].replace("\n", " ")
            has = any(l in ctx for l in LAYER)
            print(f"{sno}/{no} | {size} | {subj} | {o} | {'Y' if has else 'N'} | {ctx}")
