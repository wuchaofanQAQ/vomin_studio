# -*- coding: utf-8 -*-
import sys, os, re, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu

# 1) 剧本 v3 → 剧本表
raw = open(os.path.join(base, "drafts", "ep01m_script_v3.md"), encoding="utf-8").read()
i = raw.find("1．")
body = raw[i:].strip()
open(os.path.join(base, "drafts", "ep01m_script_body.md"), "w", encoding="utf-8").write(body + "\n")
ws.save_json("episodes.json", [{"episode": "1", "title": "我是沈幼怡",
                                "source_chapters": "1", "script": body, "status": "草稿"}])
tid = ws.config["feishu"]["tables"]["剧本表"]
val = ("角色：陈诚、沈幼怡\n"
       "场景：陈诚公寓走廊、陈诚公寓客厅、陈诚公寓玄关\n"
       "道具：手机、行李箱、双肩书包")
for r in fb.list_records(tid):
    f = r["fields"]
    no = f.get("集号"); no = no[0]["text"] if isinstance(no, list) else no
    if str(no) == "1":
        fb.update_record(tid, r["record_id"], {"完整剧本": body, "对应原小说章节": "1", "涉及资产": val})
print("剧本表已更新:", len(body), "字")

# 2) 分镜：3 段，删 p04
sb = ws.config["feishu"]["tables"]["剧本分镜表"]
for r in fb.list_records(sb):
    sid = r["fields"].get("镜头编号")
    sid = sid[0]["text"] if isinstance(sid, list) else sid
    if str(sid) == "ep01_p04":
        requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{sb}/records/{r['record_id']}"),
                        headers=fb._headers())
        print("删除 ep01_p04")

md = open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜\[0s-[\d.]+s\]｜.+?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    header, seg = parts[i], parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜\[0s-([\d.]+)s\]｜(.+?)】", header)
    no, dur, title = int(m.group(1)), float(m.group(2)), m.group(3)
    rows.append({"shot_id": f"ep01_p{no:02d}", "episode": 1, "title": title,
                 "timeline": f"0s-{dur:g}s", "prompt": "## " + header + "\n\n" + seg, "status": "待生成"})
json.dump(rows, open(os.path.join(base, "drafts", "ep01m_shots.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
local = [r for r in ws.load_storyboard() if r.get("shot_id") != "ep01_p04"]
ws.save_json("storyboard.json", local)
print("rows:", [r["shot_id"] for r in rows])
