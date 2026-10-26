# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_script_v1.md"
t = open(p, encoding="utf-8").read()

old = """△他凑到猫眼上。猫眼里，她还站在原地，手搭着行李箱拉杆。
陈诚（低骂）：靠。
△他一把拉开门，从鞋柜里拎出双旧拖鞋，扔到她脚边。
陈诚：穿上。"""
new = """△他凑到猫眼上。猫眼里，她还站在原地，手搭着行李箱拉杆。
陈诚（低骂）：靠。
陈诚（OS、急了）：听不懂人话是吧？这天再晒下去真会出人命的。
△他一把拉开门，侧身让出半个门洞。
陈诚（语气冲）：进不进？中暑了我可没钱送你去医院。
△他从鞋柜里拎出双旧拖鞋，扔到她脚边。
陈诚：穿上。"""

assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)

import re
lines = [l for l in t.splitlines() if l.strip()]
dlg = [l for l in lines if re.match(r"^[^△（].{0,8}(（[^）]*）)?：", l)]
beats = [l for l in lines if l.startswith("△")]
speech = sum(len(re.sub(r"[^\u4e00-\u9fff]", "", d.split("：", 1)[-1])) / 5 for d in dlg)
print("台词:", len(dlg), "| 动作:", len(beats))
print("估算: %.0fs" % (speech + len(beats) * 2.2))
