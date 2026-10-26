# -*- coding: utf-8 -*-
import sys, os, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tables = ws.config["feishu"]["tables"]
ep_tid = tables["剧本表"]
sb_tid = tables["剧本分镜表"]

script = open(os.path.join(base, "drafts", "ep01m_script_v1.md"), encoding="utf-8").read()

# 1) 剧本表：更新集数 1
eps = fb.list_records(ep_tid)
rec1 = None
for r in eps:
    v = r.get("fields", {}).get("集数")
    v = v[0]["text"] if isinstance(v, list) and v else v
    if str(v) == "1":
        rec1 = r["record_id"]
if rec1:
    fb.update_record(ep_tid, rec1, {
        "集名": "我是沈幼怡",
        "对应原小说章节": "1,2",
        "完整剧本": script,
        "状态": "草稿",
    })
    print("剧本表 集数1 已更新为新版")
else:
    fb.create_record(ep_tid, {"集数": "1", "集名": "我是沈幼怡", "对应原小说章节": "1,2",
                              "完整剧本": script, "状态": "草稿"})
    print("剧本表 集数1 已创建")

# 2) 删剧本表 2、3
for r in fb.list_records(ep_tid):
    v = r.get("fields", {}).get("集数")
    v = v[0]["text"] if isinstance(v, list) and v else v
    if str(v) in ("2", "3"):
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{ep_tid}/records/{r['record_id']}"),
                        headers=fb._headers())
        print("删除旧剧本 集数", v)

# 3) 删分镜表旧行（ep01/ep02/ep03）
n = 0
for r in fb.list_records(sb_tid):
    sid = r.get("fields", {}).get("镜头编号")
    sid = sid[0]["text"] if isinstance(sid, list) and sid else sid
    if str(sid).startswith(("ep01_", "ep02_", "ep03_")):
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{sb_tid}/records/{r['record_id']}"),
                        headers=fb._headers())
        n += 1
print("删除旧分镜行:", n)

# 4) 本地同步
ws.save_json("episodes.json", [{
    "episode": "1", "title": "我是沈幼怡", "source_chapters": "1,2",
    "script": script, "status": "草稿",
}])
ws.save_json("storyboard.json", [])
fb.pull_episodes(ws)
fb.pull_storyboard(ws)
print("本地已同步；分镜表剩余", len(ws.load_storyboard()), "条")
