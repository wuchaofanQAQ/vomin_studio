# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
val = "\n".join([
    "角色：陈诚、沈幼怡",
    "场景：陈诚公寓走廊、陈诚公寓玄关、陈诚公寓客厅傍晚、陈诚公寓玄关傍晚",
    "道具：手机、黑拖鞋、行李箱、双肩书包、玻璃杯",
])
for r in fb.list_records(tid):
    f = r["fields"]
    no = f.get("集号"); no = no[0]["text"] if isinstance(no, list) else no
    if str(no) == "1":
        fb.update_record(tid, r["record_id"], {"涉及资产": val})
print(val)
