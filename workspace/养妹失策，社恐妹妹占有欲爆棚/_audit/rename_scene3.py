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
tid = ws.config["feishu"]["tables"]["资产库"]

RENAME = {
    "陈诚公寓客厅反打": ("陈诚公寓玄关",
        "【陈诚公寓客厅】的反打：从沙发位置看向入户门。近景：画面右下的沙发扶手、地毯边缘与茶几一角；中景：餐桌与四把餐椅、画左的电视柜与电视墙；远景：黑色入户门居中、门左边柜与洞洞板、门右开放式厨房与白色冰箱。白天光。"),
    "陈诚公寓客厅傍晚反打": ("陈诚公寓玄关傍晚",
        "同【陈诚公寓玄关】：同一空间、同一机位，只把光影换成傍晚（与【陈诚公寓客厅傍晚】一致）。近景：沙发扶手与地毯上被拉长的窗影；中景：餐桌椅与电视柜（暖橘反光）；远景：入户门、边柜、开放式厨房与冰箱，暗部压深。"),
    "陈诚公寓客厅": ("陈诚公寓客厅",
        "从入户方向看客厅（正打）。近景：地毯与木地板；中景：白色布艺沙发、矮茶几、单人扶手椅；远景：尽头大窗与城市景、窗帘、画右电视墙、左侧通玄关的门洞。白天光。"),
    "陈诚公寓客厅傍晚": ("陈诚公寓客厅傍晚",
        "同【陈诚公寓客厅】：同一空间、同一机位，只把光影换成傍晚。近景：地毯上的斜长窗影；中景：沙发、茶几与单人椅（暖橘反光）；远景：尽头大窗的落日、窗帘、画右电视墙压暗。"),
}

for r in fb.list_records(tid):
    f = r["fields"]
    nm = f.get("名称"); nm = nm[0]["text"] if isinstance(nm, list) else nm
    if nm in RENAME:
        new, note = RENAME[nm]
        fb.update_record(tid, r["record_id"], {"名称": new, "备注": note})
        print("更新:", nm, "->", new)

# 分镜同步改名（先长后短）
f2 = os.path.join(base, "drafts", "ep01m_storyboard_v1.md")
s = open(f2, encoding="utf-8").read()
s = s.replace("陈诚公寓客厅傍晚反打", "陈诚公寓玄关傍晚")
s = s.replace("陈诚公寓客厅反打", "陈诚公寓玄关")
open(f2, "w", encoding="utf-8").write(s)
print("分镜已同步")
