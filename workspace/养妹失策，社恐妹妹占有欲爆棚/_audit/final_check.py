# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
fb = ws.feishu
print("表:", sorted(fb.discover_tables().keys()))

tid = ws.config["feishu"]["tables"]["资产库"]
rows = fb.list_records(tid)
print("资产库:", len(rows))

tid2 = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid2):
    f = r["fields"]
    v = f.get("涉及资产")
    v = "".join(x.get("text", "") for x in v) if isinstance(v, list) else (v or "")
    try:
        arr = json.loads(v) if v else []
    except Exception:
        arr = []
    print("剧本表 集号", f.get("集号"), "| 涉及资产", len(arr), "条 | 首条", arr[0] if arr else None)

tid3 = ws.config["feishu"]["tables"]["剧本分镜表"]
print("分镜:", [(r["fields"].get("镜头编号")) for r in fb.list_records(tid3)])
