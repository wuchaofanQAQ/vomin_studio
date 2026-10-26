# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
p = os.path.join(base, "drafts", "ep01m_script_body.md")
s = open(p, encoding="utf-8").read()

# 1) 门口初见：补「来投奔亲戚的？」
old1 = "△陈诚的脸僵住。闪回半秒：蛋糕、砸碎的白碗、女人跟着西装男人出门。"
new1 = ("△陈诚的视线从她脸上扫到行李箱，又扫回她脸上。\n"
        "陈诚（OS）：来投奔亲戚的？\n"
        "△陈诚的脸僵住。闪回半秒：蛋糕、砸碎的白碗、女人跟着西装男人出门。")
assert s.count(old1) == 1
s = s.replace(old1, new1)

# 2) 掏手机：补顶配特写 + 房租对比 + 哑巴猜测
old2 = "△她从兜里掏出一部最新款的苹果手机，敲了几下，举到他面前。"
new2 = ("△她从兜里掏出一部最新款的苹果手机，机身上的原厂膜还没撕。\n"
        "△特写：钛金属边框，背面三颗摄像头，镜头圈亮得晃眼。\n"
        "陈诚（OS）：顶配。那手机够他三个月房租。\n"
        "陈诚（OS）：哑巴？还是不想说话。\n"
        "△她敲了几下，把屏幕举到他面前。")
assert s.count(old2) == 1
s = s.replace(old2, new2)

open(p, "w", encoding="utf-8").write(s)
print("剧本已补爽点")

# 3) 同步到剧本表（body 写回 episodes.json + 飞书）
ws.save_json("episodes.json", [{
    "episode": "1", "title": "我是沈幼怡", "source_chapters": "1,2",
    "script": s, "status": "草稿",
}])
fb = ws.feishu
tid = ws.config["feishu"]["tables"]["剧本表"]
for r in fb.list_records(tid):
    f = r["fields"]
    no = f.get("集号"); no = no[0]["text"] if isinstance(no, list) else no
    if str(no) == "1":
        fb.update_record(tid, r["record_id"], {"完整剧本": s})
print("剧本表已更新")
