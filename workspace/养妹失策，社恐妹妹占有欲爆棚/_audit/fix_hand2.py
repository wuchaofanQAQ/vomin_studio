# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

i = t.index("【镜头10｜")
j = t.index("\n\n", i)
old = t[i:j]

new = """【镜头10｜[19s-21.5s]｜旧疤】
回忆手持特写，四角压暗，镜头轻晃。屋里只有一盏偏黄的顶灯，光发闷，桌面上反着一层油光；夏夜的风扇声在画外一下一下地响。旧木桌上插着蜡烛的方形蛋糕，奶油发干起皮、塌了一角。画面里没有人物：只有一只**成年男人的手**从画左探进来——手掌宽厚、指节粗大、手背浮着青筋，袖口是洗旧的白背心短袖，手腕上有一道旧疤；这只手一把扣住桌沿，把桌边的白瓷碗扫下桌沿，碗砸在地上，瓷片朝画左下方迸开，其中一片在地上打转、慢慢停住；手扫完立刻抽回画外，只留下还在晃的桌角。切在最后那片碎片停稳之前。"""

t = t[:i] + new + t[j:]
open(f, "w", encoding="utf-8").write(t)
print("镜头10 重写：明确是他父亲的手")
