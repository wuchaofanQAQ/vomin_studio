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
tid = ws.config["feishu"]["tables"]["资产库"]
root = f"bitable/v1/apps/{fb.app_token}/tables/{tid}"

# 1) 加 备注，删 ID
fields = {f["field_name"]: f["field_id"] for f in requests.get(api(f"{root}/fields"), headers=h).json()["data"]["items"]}
if "备注" not in fields:
    requests.post(api(f"{root}/fields"), headers=h, json={"field_name": "备注", "type": 1})
    print("加字段 备注")
if "ID" in fields:
    requests.delete(api(f"{root}/fields/{fields['ID']}"), headers=h)
    print("删字段 ID")

RENAME = {
    "陈诚公寓客厅（反打玄关）": ("陈诚公寓客厅反打", "从沙发位反打入户门：电视墙在左、黑门居中、右侧开放厨房与餐桌。白天光。"),
    "陈诚公寓客厅（傍晚）": ("陈诚公寓客厅傍晚", "同客厅布局，夕阳从尽头大窗斜切，主灯未开，暗部压深。"),
    "陈诚公寓客厅（傍晚·反打玄关）": ("陈诚公寓客厅傍晚反打", "反打角度，夕阳从机位后方大窗照入，地板拉长影。"),
}
DELETE = {"陈诚公寓玄关客厅（傍晚）", "陈诚公寓玄关客厅（夜）", "陈诚公寓阳台"}

recs = fb.list_records(tid)
for r in recs:
    f = r["fields"]
    nm = f.get("名称"); nm = nm[0]["text"] if isinstance(nm, list) and nm else nm
    if nm in RENAME:
        new, note = RENAME[nm]
        fb.update_record(tid, r["record_id"], {"名称": new, "备注": note})
        print("改名:", nm, "->", new)
    elif nm in DELETE:
        requests.delete(api(f"{root}/records/{r['record_id']}"), headers=h)
        print("删除未使用场景:", nm)

print("剩余资产:", len(fb.list_records(tid)))
