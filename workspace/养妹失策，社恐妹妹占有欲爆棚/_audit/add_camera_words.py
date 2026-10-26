# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
pairs = [
("切镜头，略偏正面的近景", "切镜头，正面机位的近景"),
("切镜头，稍偏正面的近景", "切镜头，正面机位的近景"),
("切镜头，手部特写", "切镜头，手部机位的特写"),
("切镜头，窗侧的中景", "切镜头，窗侧机位的中景"),
("切镜头，与【沈幼怡】下巴同高的近景", "切镜头，与【沈幼怡】下巴同高的机位近景"),
("切镜头，客厅中央的中景", "切镜头，客厅中央机位的中景"),
("切镜头，反打机位的中景", "切镜头，反打机位的中景"),
]
for a, b in pairs:
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("机位词补齐")
