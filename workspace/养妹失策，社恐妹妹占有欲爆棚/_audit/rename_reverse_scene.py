# -*- coding: utf-8 -*-
import sys, os, json, re, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
OLD, NEW = "陈诚公寓玄关", "陈诚公寓客厅（反打玄关）"
ws = Workspace(base)

# 1) 场景库改名（本地 + 飞书）
scenes = ws.load_json("scenes.json")
for s in scenes:
    if s.get("name") == OLD:
        s["name"] = NEW
        s["description"] = "从沙发方向反打入户门：电视墙在画左，黑色入户门居中，右侧开放式厨房与餐桌，玄关柜在门左。"
ws.save_json("scenes.json", scenes)
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["场景库"]
for r in fb.list_records(tid):
    nm = r["fields"].get("场景ID")
    nm = nm[0]["text"] if isinstance(nm, list) and nm else nm
    if nm == OLD:
        fb.update_record(tid, r["record_id"], {
            "场景ID": NEW,
            "场景描述": "从沙发方向反打入户门：电视墙在画左，黑色入户门居中，右侧开放式厨房与餐桌，玄关柜在门左。",
        })
        print("飞书场景已改名")
print("本地场景已改名")

# 2) 分镜替换 + p04 补锁
f = os.path.join(base, "drafts", "ep01m_storyboard_v1.md")
s = open(f, encoding="utf-8").read()
s = s.replace(OLD, NEW)

parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    if f"【{NEW}】：" not in body and "走回客厅中央" in body:
        lock_end = body.index("【本段现场生成】")
        body = body[:lock_end].rstrip("\n") + f"\n【{NEW}】：{{场景库：{NEW}}}\n\n" + body[lock_end:]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    names = re.findall(r"^【([^】]+)】：\{", lock, re.M)
    mapping = "【参考图映射】" + "；".join(f"图{n+1}=【{nm}】" for n, nm in enumerate(names))
    lock = re.sub(r"【参考图映射】[^\n]+", mapping, lock, count=1)
    res += [head, lock + rest]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("分镜已替换 + p04 补锁")
