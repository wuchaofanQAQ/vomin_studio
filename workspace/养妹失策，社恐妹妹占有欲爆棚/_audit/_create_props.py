# -*- coding: utf-8 -*-
import os, sys, shutil, yaml
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

root = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
cfg = os.path.join(root, "workspace.yaml")
shutil.copyfile(cfg, os.path.join(root, "_audit", "workspace.yaml.bak"))

ws = Workspace(root)
feis = ws.feishu
tables = feis.discover_tables()
all_tables = feis.ensure_tables(tables)
tid = all_tables.get("道具库")
print("道具库 table_id:", tid)

# 字段清单
import requests
h = feis._headers()
base = f"bitable/v1/apps/{feis.app_token}"
r = requests.get(f"https://open.feishu.cn/open-apis/{base}/tables/{tid}/fields", headers=h)
print("fields:", [f["field_name"] for f in r.json()["data"]["items"]])

d = yaml.safe_load(open(cfg, encoding="utf-8"))
d["feishu"]["tables"]["道具库"] = tid
with open(cfg, "w", encoding="utf-8") as f:
    yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False)
print("workspace.yaml updated")
