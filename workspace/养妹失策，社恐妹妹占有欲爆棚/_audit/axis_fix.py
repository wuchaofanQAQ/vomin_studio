# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
pairs = [
("【陈诚】的目光从画右画外扫到画外下方", "【陈诚】的目光从画左画外扫到画外下方"),
("【陈诚】盯着画右画外看了两秒", "【陈诚】盯着画左画外看了两秒"),
("他的视线越过手机，落向画右画外", "他的视线越过手机，落向画左画外"),
("他的视线越过举在面前的手机，落向画右画外", "他的视线越过举在面前的手机，落向画左画外"),
("他的视线重新聚焦到画右画外", "他的视线重新聚焦到画左画外"),
("【陈诚】的目光落回画右画外", "【陈诚】的目光落回画左画外"),
("【陈诚】的视线在画右画外与画外下方之间来回", "【陈诚】的视线在画左画外与画外下方之间来回"),
("视线别开，落在画左的走廊尽头", "视线别开，落向门框一侧的画外"),
]
for a, b in pairs:
    c = t.count(a)
    print(c, a[:30])
    assert c >= 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("axis fixed")
