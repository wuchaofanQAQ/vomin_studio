# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
shots = ws.load_storyboard()
parts = []
for s in shots:
    p = s["prompt"].strip()
    if not p.startswith("## "):
        p = "## " + p
    parts.append(p)
open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
print("restored with ## prefix:", len(parts))
