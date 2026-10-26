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
h = fb._headers()
api = fb._api
root = f"bitable/v1/apps/{fb.app_token}"
tables = dict(ws.config["feishu"]["tables"])

if "资产库" in tables:
    print("资产库已存在:", tables["资产库"]); sys.exit(0)

r = requests.post(api(f"{root}/tables"), headers=h, json={"table": {"name": "资产库"}}, timeout=20)
r.raise_for_status()
tid = r.json()["data"]["table_id"]
print("created:", tid)

# 主字段改名 名称，删掉其他默认字段
fields = requests.get(api(f"{root}/tables/{tid}/fields"), headers=h).json()["data"]["items"]
for f in fields:
    if f.get("is_primary"):
        requests.put(api(f"{root}/tables/{tid}/fields/{f['field_id']}"), headers=h,
                     json={"field_name": "名称", "type": 1})
for f in fields:
    if not f.get("is_primary"):
        requests.delete(api(f"{root}/tables/{tid}/fields/{f['field_id']}"), headers=h)

for fd in [
    {"field_name": "ID", "type": 2},
    {"field_name": "类型", "type": 3, "property": {"options": [{"name": "角色"}, {"name": "场景"}, {"name": "道具"}]}},
    {"field_name": "描述", "type": 1},
    {"field_name": "文件路径", "type": 1},
]:
    requests.post(api(f"{root}/tables/{tid}/fields"), headers=h, json=fd)
    time.sleep(0.15)

# 迁移数据：角色 → 场景 → 道具
chars = ws.load_json("characters.json")
scenes = ws.load_json("scenes.json")
props = ws.load_json("props.json")
rows, nid = [], 1
for c in chars:
    rows.append({"ID": nid, "名称": c["name"], "类型": "角色", "描述": c.get("appearance", ""), "文件路径": c.get("ref_image") or ""})
    nid += 1
for s in scenes:
    rows.append({"ID": nid, "名称": s["name"], "类型": "场景", "描述": s.get("description", ""), "文件路径": s.get("ref_image") or ""})
    nid += 1
for p in props:
    rows.append({"ID": nid, "名称": p["name"], "类型": "道具", "描述": p.get("description", ""), "文件路径": p.get("ref_image") or ""})
    nid += 1

for b in range(0, len(rows), 20):
    requests.post(api(f"{root}/tables/{tid}/records/batch_create"), headers=h,
                  json={"records": [{"fields": x} for x in rows[b:b+20]]}, timeout=30)
    time.sleep(0.3)

back = fb.list_records(tid)
print("rows:", len(back))
for r_ in back[:5]:
    f = r_["fields"]
    print(" ", f.get("ID"), f.get("名称"), f.get("类型"))

tables["资产库"] = tid
ws.config["feishu"]["tables"] = tables
ws.save_config()
print("workspace.yaml 已登记 资产库")
