# -*- coding: utf-8 -*-
"""清空飞书剧本分镜表全部记录（batch delete），供重写重构版分镜"""
import os, io, requests
from dotenv import load_dotenv
load_dotenv(r"C:\Users\Heart\PycharmProjects\vomin_studio\.env")
APP_TOKEN = "UWhZbNm8ba7fUlsC0WqcetrJnsd"
TABLE_ID = "tblxFQ18PyGiRwcT"

def get_token():
    r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                      json={"app_id": os.environ["FEISHU_APP_ID"], "app_secret": os.environ["FEISHU_APP_SECRET"]}, timeout=15)
    return r.json()["tenant_access_token"]

tok = get_token()
H = {"Authorization": "Bearer " + tok, "Content-Type": "application/json"}

# 1. 拉全部记录 id
recs = []
page_token = None
while True:
    params = {"page_size": 100}
    if page_token:
        params["page_token"] = page_token
    r = requests.get("https://open.feishu.cn/open-apis/bitable/v1/apps/%s/tables/%s/records" % (APP_TOKEN, TABLE_ID),
                     headers=H, params=params, timeout=15)
    d = r.json()
    items = d.get("data", {}).get("items", [])
    recs.extend(items)
    if not d.get("data", {}).get("has_more"):
        break
    page_token = d["data"].get("page_token")

ids = [x["record_id"] for x in recs]
out = ["records=%d" % len(ids)]

# 2. 分批删除（每批50）
for i in range(0, len(ids), 50):
    batch = ids[i:i+50]
    r = requests.post("https://open.feishu.cn/open-apis/bitable/v1/apps/%s/tables/%s/records/batch_delete" % (APP_TOKEN, TABLE_ID),
                      headers=H, json={"records": batch}, timeout=15)
    out.append("batch %d-%d: %s %s" % (i, i+len(batch)-1, r.status_code, r.json().get("code")))

io.open(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚_draft\del_records.log", "w", encoding="utf-8").write("\n".join(out))
print("done see del_records.log")
