# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_script_v1.md"
t = open(p, encoding="utf-8").read()

# 只合并冗余动作，不删任何台词/爽点
pairs = [
("△陈诚的脸僵住。闪回半秒：插着蜡烛的蛋糕、砸碎的白碗、女人跟着深灰西装男人出门。",
 "△陈诚的脸僵住。闪回半秒：蛋糕、砸碎的白碗、女人跟着西装男人出门。"),
("△他挂断，手撑着栏杆。阳台外，天蓝得刺眼。",
 "△他挂断，手撑栏杆。阳台外天蓝得刺眼。"),
("△陈诚推开门，她站在客厅中央，双手捧着那杯温水，一口没动。",
 "△陈诚推门进来。她站在客厅中央，捧着那杯水，一口没动。"),
]
for a, b in pairs:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)

import re
lines = [l for l in t.splitlines() if l.strip()]
dlg = [l for l in lines if re.match(r"^[^△（].{0,8}(（[^）]*）)?：", l)]
beats = [l for l in lines if l.startswith("△")]
speech = sum(len(re.sub(r"[^\u4e00-\u9fff]", "", d.split("：", 1)[-1])) / 5 for d in dlg)
print("台词:", len(dlg), "| 动作:", len(beats), "| 估算: %.0fs" % (speech + len(beats) * 2.2))
