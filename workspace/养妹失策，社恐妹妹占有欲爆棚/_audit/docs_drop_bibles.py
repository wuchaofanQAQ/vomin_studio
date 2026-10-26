# -*- coding: utf-8 -*-
import re, glob
files = [
    r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\ai-drama-harness\SKILL.md",
    r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-initializer\SKILL.md",
    r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-extraction\SKILL.md",
    r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md",
    r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py",
]
for p in files:
    t = open(p, encoding="utf-8").read()
    n0 = t.count("角色档案")
    t = t.replace("角色库/角色档案", "角色库")
    t = t.replace("角色库 + 角色档案", "角色库")
    t = t.replace("角色档案 ×6 行", "角色库 ×6 行")
    t = t.replace("角色档案（含形象图）", "角色库（含形象图）")
    t = t.replace("剧本设定 + 角色档案", "剧本设定 + 角色库")
    t = t.replace("不写角色档案/音色", "不写人物小传/音色")
    t = t.replace("不写角色档案", "不写人物小传")
    # 删掉整行 write 角色档案 命令
    t = "\n".join(l for l in t.splitlines()
                  if "角色档案" not in l or ("read" in l and "角色档案" in l and False))
    t = t.replace("角色档案", "角色库")
    open(p, "w", encoding="utf-8").write(t)
    print(p.split("\\")[-2] + "/" + p.split("\\")[-1], "角色档案:", n0, "->", t.count("角色档案"))
