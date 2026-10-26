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
raw = open(os.path.join(base, "drafts", "ep01m_script_v1.md"), encoding="utf-8").read()

# 只保留正文：从第一个场次开始，到（本集完）之前
i = raw.find("1．")
j = raw.find("（本集完）")
body = raw[i:j].strip() if i != -1 else raw.strip()
open(os.path.join(base, "drafts", "ep01m_script_body.md"), "w", encoding="utf-8").write(body + "\n")
print("正文首行:", body.splitlines()[0])
print("正文字数:", len(body))

# 更新飞书剧本表
tid = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid):
    v = r.get("fields", {}).get("集数")
    v = v[0]["text"] if isinstance(v, list) and v else v
    if str(v) == "1":
        fb.update_record(tid, r["record_id"], {"完整剧本": body})
        print("已更新飞书 完整剧本（无剧名/集头/本集完）")

# 本地
ws.save_json("episodes.json", [{
    "episode": "1", "title": "我是沈幼怡", "source_chapters": "1,2",
    "script": body, "status": "草稿",
}])
print("本地 episodes.json 已更新")
