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
tid = ws.config["feishu"]["tables"]["剧本表"]
h = fb._headers()
api = fb._api
root = f"bitable/v1/apps/{fb.app_token}/tables/{tid}"

# 1) 备份
recs = fb.list_records(tid)
backup = []
for r in recs:
    f = r.get("fields", {})
    backup.append({k: (v if isinstance(v, str) else str(v)) for k, v in f.items()})
os.makedirs(os.path.join(base, "bak"), exist_ok=True)
bak_path = os.path.join(base, "bak", f"剧本表_迁移备份_{time.strftime('%Y%m%d_%H%M%S')}.json")
json.dump(backup, open(bak_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("已备份:", bak_path, len(backup), "条")

# 2) 删字段
fields = requests.get(api(f"{root}/fields"), headers=h).json()["data"]["items"]
fid = {f["field_name"]: f["field_id"] for f in fields}
for name in ("小说章节", "小说内容"):
    if name in fid:
        r = requests.delete(api(f"{root}/fields/{fid[name]}"), headers=h)
        print("删除字段", name, r.status_code, r.json().get("msg"))
        time.sleep(0.3)

# 3) 加字段
if "对应原小说章节" not in fid:
    r = requests.post(api(f"{root}/fields"), headers=h,
                      json={"field_name": "对应原小说章节", "type": 1})
    print("新增字段 对应原小说章节", r.status_code, r.json().get("msg"))

# 4) 写值（现在每集对应 1 章）
mapping = {"1": "1", "2": "2", "3": "3"}
for r in fb.list_records(tid):
    f = r.get("fields", {})
    ep = f.get("集数")
    ep = ep[0]["text"] if isinstance(ep, list) and ep else ep
    if ep in mapping:
        fb.update_record(tid, r["record_id"], {"对应原小说章节": mapping[ep]})
        print("更新", ep, "->", mapping[ep])

# 5) 回读
fields2 = requests.get(api(f"{root}/fields"), headers=h).json()["data"]["items"]
print("现有字段:", [f["field_name"] for f in fields2])
for r in fb.list_records(tid):
    f = r.get("fields", {})
    print(" ", f.get("集数"), "|", f.get("对应原小说章节"))
