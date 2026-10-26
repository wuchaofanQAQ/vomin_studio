# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
shots = ws.load_storyboard()   # 从飞书拉取（上一版完好的）
print("rows:", len(shots))
md = "\n\n".join(s["prompt"].strip() for s in shots) + "\n"
open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), "w", encoding="utf-8").write(md)
print("已从飞书恢复分镜文件")
