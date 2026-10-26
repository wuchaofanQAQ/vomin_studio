# -*- coding: utf-8 -*-
import sys, os, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

# 1) 代码：schema + pull/push
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
t = t.replace('''                {"field_name": "小说章节", "type": 1},
                {"field_name": "小说内容", "type": 1},''',
              '''                {"field_name": "对应原小说章节", "type": 1},''')
t = t.replace('''                "novel_chapter": _text_val(f.get("小说章节", "")),
                "novel_text": _text_val(f.get("小说内容", "")),''',
              '''                "source_chapters": _text_val(f.get("对应原小说章节", "")),''')
t = t.replace('''                "小说章节": ep.get("novel_chapter", ""),
                "小说内容": ep.get("novel_text", ""),''',
              '''                "对应原小说章节": ep.get("source_chapters", ""),''')
open(p, "w", encoding="utf-8").write(t)
print("bitable 剧本表 schema/pull/push 已更新")

# 2) 本地数据迁移：novel_chapter → source_chapters
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
eps = ws.load_json("episodes.json")
for e in eps:
    if "source_chapters" not in e:
        e["source_chapters"] = str(e.get("novel_chapter") or e.get("episode") or "")
    e.pop("novel_chapter", None)
ws.save_json("episodes.json", eps)
print("本地 episodes.json:", [(e["episode"], e.get("source_chapters")) for e in eps])

# 3) 删空行
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid):
    f = r.get("fields", {})
    if not f.get("集数"):
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}/records/{r['record_id']}"),
                        headers=fb._headers())
        print("已删空行", r["record_id"])

# 4) 回读
rows = fb.pull_episodes(ws)
for e in rows:
    print(" ", e["episode"], "|", e["title"], "| 章节:", e.get("source_chapters"))
