# -*- coding: utf-8 -*-
import sys, os, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
p = os.path.join(base, "storyboard.json")
rows = json.load(open(p, encoding="utf-8"))
keep = [r for r in rows if r.get("shot_id") != "ep01_p05"]
json.dump(keep, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("local rows:", len(rows), "->", len(keep))

fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本分镜表"]
for r in fb.list_records(tid):
    sid = r["fields"].get("镜头编号")
    sid = sid[0]["text"] if isinstance(sid, list) and sid else sid
    if str(sid) == "ep01_p05":
        rid = r["record_id"]
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}/records/{rid}"),
                        headers=fb._headers())
        print("deleted ep01_p05")

rows = fb.list_records(tid)
print("分镜行数:", len(rows))
for r in rows:
    f = r["fields"]
    t = f.get("时间线"); t = t[0]["text"] if isinstance(t, list) and t else t
    print(" ", f.get("镜头编号"), "| 集号:", f.get("集号"), "|", t)
