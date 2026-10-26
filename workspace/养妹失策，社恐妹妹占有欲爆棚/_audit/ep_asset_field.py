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
h = fb._headers(); api = fb._api
root = f"bitable/v1/apps/{fb.app_token}"

ast_tid = ws.config["feishu"]["tables"]["资产库"]
ep_tid = ws.config["feishu"]["tables"]["剧本表"]

# 1) 剧本表加「涉及资产」
fields = requests.get(api(f"{root}/tables/{ep_tid}/fields"), headers=h).json()["data"]["items"]
names = [f["field_name"] for f in fields]
if "涉及资产" not in names:
    requests.post(api(f"{root}/tables/{ep_tid}/fields"), headers=h,
                  json={"field_name": "涉及资产", "type": 1})
    print("字段 涉及资产 已加")

# 2) 资产名 → ID
idx = {}
for r in fb.list_records(ast_tid):
    f = r["fields"]
    nm = f.get("名称"); nm = nm[0]["text"] if isinstance(nm, list) and nm else nm
    fid = f.get("ID")
    idx[nm] = int(fid) if fid is not None else None

used = ["陈诚", "沈幼怡", "陈诚公寓走廊", "陈诚公寓客厅（反打玄关）",
        "陈诚公寓客厅（傍晚）", "陈诚公寓客厅（傍晚·反打玄关）",
        "手机", "黑拖鞋", "行李箱", "双肩书包", "玻璃杯"]
arr = [{"ID": idx[n], "名称": n} for n in used if idx.get(n) is not None]
val = json.dumps(arr, ensure_ascii=False)
print("涉及资产:", val)

for r in fb.list_records(ep_tid):
    f = r["fields"]
    no = f.get("集号"); no = no[0]["text"] if isinstance(no, list) and no else no
    if str(no) == "1":
        fb.update_record(ep_tid, r["record_id"], {"涉及资产": val})
        print("剧本表 ep1 已写入涉及资产")
