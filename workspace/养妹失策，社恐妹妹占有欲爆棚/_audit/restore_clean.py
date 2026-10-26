# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
shots = ws.load_storyboard()   # 飞书：3.6s 版本，0 错
parts = []
for s in shots:
    p = s["prompt"].strip()
    parts.append(p if p.startswith("## ") else "## " + p)
md = "\n\n".join(parts) + "\n"
open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), "w", encoding="utf-8").write(md)
print("已从飞书恢复:", len(parts), "段")
