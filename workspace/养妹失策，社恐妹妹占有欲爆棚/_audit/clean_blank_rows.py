# -*- coding: utf-8 -*-
import sys, os, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本分镜表"]
for r in fb.list_records(tid):
    f = r["fields"]
    sid = f.get("镜头编号")
    sid = sid[0]["text"] if isinstance(sid, list) else sid
    if not sid:
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}/records/{r['record_id']}"),
                        headers=fb._headers())
        print("删除空行", r["record_id"])
rows = fb.list_records(tid)
print("剩余:", [(x["fields"].get("镜头编号"), x["fields"].get("时间线")) for x in rows])
