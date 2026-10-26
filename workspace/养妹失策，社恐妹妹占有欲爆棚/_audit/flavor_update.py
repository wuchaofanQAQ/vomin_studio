# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)

# 1) 剧本 v2 → 只取正文（从「1．」开始）
raw = open(os.path.join(base, "drafts", "ep01m_script_v2.md"), encoding="utf-8").read()
i = raw.find("1．")
body = raw[i:].strip()
open(os.path.join(base, "drafts", "ep01m_script_body.md"), "w", encoding="utf-8").write(body + "\n")
print("剧本身字数:", len(body))

ws.save_json("episodes.json", [{"episode": "1", "title": "我是沈幼怡",
                                "source_chapters": "1,2", "script": body, "status": "草稿"}])
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid):
    f = r["fields"]
    no = f.get("集号"); no = no[0]["text"] if isinstance(no, list) else no
    if str(no) == "1":
        fb.update_record(tid, r["record_id"], {"完整剧本": body})
print("剧本表已更新")

# 2) 分镜补三句小说味道的 OS
f = os.path.join(base, "drafts", "ep01m_storyboard_v1.md")
s = open(f, encoding="utf-8").read()
s = s.replace("""切在【手机】翻正、背面朝镜头。
""", """切在【手机】翻正、背面朝镜头。
[4.2s-5.6s]，【陈诚】（OS、心里咯噔一下说）：「这哪是找错门，是找错小区了。」
""")
s = s.replace("""（字幕·微信）「你帮妈照看一阵子，就一阵子……」
""", """（字幕·微信）「你帮妈照看一阵子，就一阵子……」
[23s-25.6s]，【陈诚】（OS、冷笑着说）：「妈？她还知道自己是妈。」
""")
open(f, "w", encoding="utf-8").write(s)
print("分镜补 OS 两处")
