# -*- coding: utf-8 -*-
import sys, os, json, time, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tables = ws.config["feishu"]["tables"]
ts = time.strftime("%Y%m%d_%H%M%S")

def dump(table_name, fname):
    tid = tables[table_name]
    recs = fb.list_records(tid)
    rows = []
    for r in recs:
        f = r.get("fields", {})
        rows.append({k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
                     for k, v in f.items()})
    path = os.path.join(base, "bak", f"{fname}_{ts}.json")
    json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("备份", table_name, len(rows), "条 ->", os.path.basename(path))
    return rows

dump("剧本表", "剧本表_旧版备份")
dump("剧本分镜表", "分镜表_旧版备份")
