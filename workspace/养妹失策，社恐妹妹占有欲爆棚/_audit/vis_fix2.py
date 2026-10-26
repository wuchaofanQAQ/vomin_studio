# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
pairs = [
("[18s-19.5s]，【陈诚】（盯着【行李箱】、低声说）", "[18s-19.5s]，【陈诚】（盯着画外下方、低声说）"),
("切在他视线第二次落回【行李箱】、眉心拧死时", "切在他视线第二次落回画外下方、眉心拧死时"),
("【镜头05｜[10s-12s]｜搭上拉杆】\n硬切近景固定机位。", "【镜头05｜[10s-12s]｜搭上拉杆】\n硬切中近景固定机位。"),
]
for a, b in pairs:
    c = t.count(a)
    print(c, a[:34].replace("\n", " "))
    assert c == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("remaining fixed")
