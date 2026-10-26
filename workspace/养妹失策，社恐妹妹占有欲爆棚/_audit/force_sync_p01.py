# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本分镜表"]
rows = {r["shot_id"]: r for r in json.load(open(os.path.join(base, "drafts", "ep01m_shots.json"), encoding="utf-8"))}

for rec in fb.list_records(tid):
    f = rec["fields"]
    sid = f.get("镜头编号"); sid = sid[0]["text"] if isinstance(sid, list) else sid
    if sid in rows:
        fb.update_record(tid, rec["record_id"], {
            "视频提示词": rows[sid]["prompt"],
            "时间线": rows[sid]["timeline"],
            "镜头标题": rows[sid]["title"],
        })
        print("updated", sid)

# 回读验证
for rec in fb.list_records(tid):
    f = rec["fields"]
    sid = f.get("镜头编号"); sid = sid[0]["text"] if isinstance(sid, list) else sid
    p = f.get("视频提示词"); p = "".join(x.get("text", "") for x in p) if isinstance(p, list) else (p or "")
    if "三条微信" in p:
        i = p.find("三条微信")
        print(sid, "| 含【手机】:", "掏出自己的【手机】" in p, "|", p[i:i+20])
