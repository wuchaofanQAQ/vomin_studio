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
h = fb._headers(); api = fb._api
tables = dict(ws.config["feishu"]["tables"])

# 备份 + 删除
for name in ("角色库", "场景库", "道具库"):
    tid = tables.get(name)
    if not tid:
        print("跳过（无 id）:", name); continue
    rows = []
    for r in fb.list_records(tid):
        f = r.get("fields", {})
        rows.append({k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in f.items()})
    path = os.path.join(base, "bak", f"{name}_删除备份_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    r = requests.delete(api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}"), headers=h)
    print(f"{name}: 备份 {len(rows)} 条 -> 删除 {r.status_code} {r.json().get('msg')}")
    tables.pop(name, None)
    time.sleep(0.3)

ws.config["feishu"]["tables"] = tables
ws.save_config()
print("剩余表:", list(tables))

# 代码：从 TABLE_SCHEMA 移除三张旧表（避免 init 重建）
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
for name in ("角色库", "场景库", "道具库"):
    import re
    t = re.sub(r'        "' + name + r'": \{.*?\n        \},\n(?=        "[^"]+": \{)', "", t, flags=re.S)
open(p, "w", encoding="utf-8").write(t)
print("TABLE_SCHEMA 已移除三表；剩余:", [k for k in __import__("re").findall(r'^        "([^"]+)": \{', t, __import__("re").M)])
