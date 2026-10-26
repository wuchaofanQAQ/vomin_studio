# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

old = "没有人物入画，只有一只手影从画面边缘掠过去。"
new = ("没有人物入画。画面左侧探进来一只成年男人的手——手掌宽厚、指节粗、手背浮着青筋，"
       "袖口是洗旧的白背心短袖，手腕上有一道旧疤；这只手一把扣住桌沿、把桌边的白瓷碗扫了下去，"
       "扫完立刻抽回画外，只留下晃动的桌角。")
assert t.count(old) == 1
t = t.replace(old, new)

# 基准里点明这只手是谁
t = t.replace("回忆转低饱和冷灰、四角压暗、细颗粒。整体低饱和灰调。",
              "回忆转低饱和冷灰、四角压暗、细颗粒。整体低饱和灰调。回忆里的手是【陈诚】父亲的手：成年男性、宽厚、指节粗，与厨房砸东西的是同一个人。")

open(f, "w", encoding="utf-8").write(t)
print("旧疤镜头的手已写清")
