# -*- coding: utf-8 -*-
import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【|\Z)", md)
SIZE = ["大特写","特写","中近景","近景","中景","全景","远景"]
WIDE = ["地砖","走廊纵深","厨房","客厅","玄关","餐桌","门洞"]
print("镜数:", len(shots))
print("=== 景别与后景冲突 ===")
for no, a, b, title, body in shots:
    head = body[:40]
    size = next((s for s in SIZE if s in head), "?")
    back = re.search(r"后景是([^；。]+)", body)
    back = back.group(1) if back else ""
    if size in ("特写","大特写","近景") and any(w in back for w in WIDE):
        print(f"  镜头{no} [{a}-{b}s] {title} | {size} | 后景:{back[:26]}")
print("=== 动作句主语缺失 ===")
for no, a, b, title, body in shots:
    for m in re.finditer(r"(从内侧拉开|被拎起|被带上|被推开|被拉开|被塞进|被推到)", body):
        pre = body[max(0, m.start()-14):m.start()]
        if "【" not in pre:
            print(f"  镜头{no} [{a}-{b}s] {title} | …{pre}{m.group(1)}")
