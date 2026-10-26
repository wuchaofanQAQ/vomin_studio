# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tables = dict(ws.config.get("feishu", {}).get("tables", {}))
print("已有表:", list(tables))

# 1) 建缺失表（小说表）
tables = fb.ensure_tables(tables)
ws.config.setdefault("feishu", {})["tables"] = tables
ws.save_config()
print("小说表 id:", tables.get("小说表"))

# 2) 用前三集 novel_text 播种 3 章
episodes = ws.load_json("episodes.json")
rows = []
for ep in episodes:
    rows.append({
        "章节": str(ep.get("episode")),
        "标题": ep.get("title", ""),
        "内容": ep.get("novel_text", ""),
    })
ws.save_json("novels.json", rows)
print("本地 novels.json:", [(r["章节"], r["标题"], len(r["内容"])) for r in rows])

# 3) 推送到飞书
fb.push_novels(ws)

# 4) 回读校验
back = fb.pull_novels(ws)
print("回读章节:", [(r["章节"], r["标题"], len(r["内容"])) for r in back])
