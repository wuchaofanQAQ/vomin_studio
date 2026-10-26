# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
recs = fb.list_records(tid)
print("飞书行数:", len(recs))
for r in recs:
    f = r.get("fields", {})
    ep = f.get("集数")
    ep = ep[0]["text"] if isinstance(ep, list) and ep else ep
    sc = f.get("完整剧本")
    if isinstance(sc, list):
        sc = "".join(x.get("text", "") for x in sc)
    print("record:", r["record_id"], "| 集数:", ep, "| 剧本长度:", len(sc or ""))
    print("  首 60 字:", (sc or "")[:60].replace("\n", " "))
