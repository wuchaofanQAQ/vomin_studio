# -*- coding: utf-8 -*-
import sys, os, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
body = open(os.path.join(base, "drafts", "ep01m_script_body.md"), encoding="utf-8").read().strip()
print("待写正文字数:", len(body))

rec = fb.list_records(tid)[0]
rid = rec["record_id"]
url = f"bitable/v1/apps/{fb.app_token}/tables/{tid}/records/{rid}"
r = requests.put(fb._api(url), headers=fb._headers(),
                 json={"fields": {"完整剧本": body}}, timeout=30)
print("PUT", r.status_code, r.json().get("code"), r.json().get("msg"))

# 直接回读
recs = fb.list_records(tid)
sc = recs[0].get("fields", {}).get("完整剧本")
if isinstance(sc, list):
    sc = "".join(x.get("text", "") for x in sc)
print("回读长度:", len(sc or ""))
print("首 40 字:", (sc or "")[:40].replace("\n", " "))
