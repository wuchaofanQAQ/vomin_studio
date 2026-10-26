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
h = fb._headers()
api = fb._api
ts = time.strftime("%Y%m%d_%H%M%S")

def fields(tid):
    return {f["field_name"]: f["field_id"] for f in
            requests.get(api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}/fields"), headers=h).json()["data"]["items"]}

# 0) 备份两张表
for name in ("剧本表", "剧本分镜表"):
    tid = tables[name]
    rows = []
    for r in fb.list_records(tid):
        f = r.get("fields", {})
        rows.append({k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in f.items()})
    path = os.path.join(base, "bak", f"{name}_改字段前_{ts}.json")
    json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("备份", name, len(rows), "条")

# 1) 剧本表：集数 → 集号
ep_tid = tables["剧本表"]
f0 = fields(ep_tid)
if "集数" in f0:
    r = requests.put(api(f"bitable/v1/apps/{fb.app_token}/tables/{ep_tid}/fields/{f0['集数']}"),
                     headers=h, json={"field_name": "集号", "type": 1})
    print("重命名 集数→集号:", r.status_code, r.json().get("msg"))

# 2) 分镜表：删人物锁定/环境锁定
sb_tid = tables["剧本分镜表"]
f1 = fields(sb_tid)
for name in ("人物锁定", "环境锁定"):
    if name in f1:
        r = requests.delete(api(f"bitable/v1/apps/{fb.app_token}/tables/{sb_tid}/fields/{f1[name]}"), headers=h)
        print("删除字段", name, r.status_code, r.json().get("msg"))

print("剧本表现有字段:", list(fields(ep_tid)))
print("分镜表现有字段:", list(fields(sb_tid)))
