# -*- coding: utf-8 -*-
import os, re, glob

root = r"C:\Users\Heart\PycharmProjects\vomin_studio"
files = [p for p in glob.glob(os.path.join(root, "skills", "**", "*.md"), recursive=True)]

for p in files:
    t0 = open(p, encoding="utf-8").read()
    t = t0
    # 复合写法先收敛
    t = t.replace("角色库/场景库/道具库", "资产库")
    t = t.replace("角色库、场景库、道具库", "资产库")
    t = t.replace("角色库 / 场景库 / 道具库", "资产库")
    t = t.replace("角色库（角色）+ 场景库（场景）+ 道具库（道具）", "资产库")
    # 单表名
    t = t.replace("角色库", "资产库").replace("场景库", "资产库").replace("道具库", "资产库")
    # 去重
    while "资产库资产库" in t:
        t = t.replace("资产库资产库", "资产库")
    if t != t0:
        open(p, "w", encoding="utf-8").write(t)
        print(os.path.relpath(p, root), "updated")
