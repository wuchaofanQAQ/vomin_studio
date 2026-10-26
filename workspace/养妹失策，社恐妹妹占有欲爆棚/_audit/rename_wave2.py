# -*- coding: utf-8 -*-
import sys, os, re, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

# ---------- 1) 代码：资产库 schema / 读写 ----------
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
t = t.replace('''                {"field_name": "ID", "type": 2},
                {"field_name": "类型", "type": 3, "property": {"options": [
                    {"name": "角色"}, {"name": "场景"}, {"name": "道具"},
                ]}},
                {"field_name": "描述", "type": 1},
                {"field_name": "文件路径", "type": 1},''',
'''                {"field_name": "类型", "type": 3, "property": {"options": [
                    {"name": "角色"}, {"name": "场景"}, {"name": "道具"},
                ]}},
                {"field_name": "描述", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "备注", "type": 1},''')
t = t.replace('''            idv = f.get("ID")
            try:
                idv = int(idv) if idv is not None else None
            except (TypeError, ValueError):
                idv = None
            rows.append({
                "id": idv,
                "name": nm,''', '''            rows.append({
                "name": nm,''')
t = t.replace('''                "description": _text_val(f.get("描述", "")),
                "file_path": _text_val(f.get("文件路径", "")),
                "_record_id": rec["record_id"],''', '''                "description": _text_val(f.get("描述", "")),
                "file_path": _text_val(f.get("文件路径", "")),
                "note": _text_val(f.get("备注", "")),
                "_record_id": rec["record_id"],''')
t = t.replace('''        rows.sort(key=lambda x: (x["id"] is None, x["id"]))
''', "")
t = t.replace('''                "名称": a.get("name", ""),
                "ID": a.get("id"),
                "类型": a.get("kind", ""),
                "描述": a.get("description", ""),
                "文件路径": a.get("file_path", ""),''', '''                "名称": a.get("name", ""),
                "类型": a.get("kind", ""),
                "描述": a.get("description", ""),
                "文件路径": a.get("file_path", ""),
                "备注": a.get("note", ""),''')
open(p, "w", encoding="utf-8").write(t)
print("bitable: 资产库 schema/读写已去 ID、加备注")

# ---------- 2) 分镜：场景改名 ----------
f = r"workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
for a, b in [("陈诚公寓客厅（傍晚·反打玄关）", "陈诚公寓客厅傍晚反打"),
             ("陈诚公寓客厅（反打玄关）", "陈诚公寓客厅反打"),
             ("陈诚公寓客厅（傍晚）", "陈诚公寓客厅傍晚")]:
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("分镜场景名已缩短")

# ---------- 3) 剧本表：涉及资产改成分行 ----------
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
lib = ws.load_assets_lib()
by_kind = {}
for a in lib:
    by_kind.setdefault(a["kind"], []).append(a["name"])
used = {
    "角色": ["陈诚", "沈幼怡"],
    "场景": ["陈诚公寓走廊", "陈诚公寓客厅反打", "陈诚公寓客厅傍晚", "陈诚公寓客厅傍晚反打"],
    "道具": ["手机", "黑拖鞋", "行李箱", "双肩书包", "玻璃杯"],
}
lines = [f"{k}：{'、'.join(v)}" for k, v in used.items()]
val = "\n".join(lines)
print(val)

fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid):
    f2 = r["fields"]
    no = f2.get("集号"); no = no[0]["text"] if isinstance(no, list) and no else no
    if str(no) == "1":
        fb.update_record(tid, r["record_id"], {"涉及资产": val})
        print("剧本表 涉及资产 已改分行")
