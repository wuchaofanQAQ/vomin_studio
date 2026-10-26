p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v12.md"
t = open(p, encoding="utf-8").read()
pairs = [
("后景是行李箱的拉杆与地砖", "后景是P01行李箱的拉杆与地砖"),
("双肩书包从肩上滑下一点", "P02双肩书包从肩上滑下一点"),
("后景是虚焦的行李箱轮子", "后景是虚焦的P01行李箱轮子"),
("前景是行李箱与鞋柜", "前景是P01行李箱与鞋柜"),
("他的视线越过沈幼怡的肩", "他的视线越过R01沈幼怡的肩"),
("他没有看沈幼怡", "他没有看R01沈幼怡"),
("前景是行李箱的轮子", "前景是P01行李箱的轮子"),
]
for a, b in pairs:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("bare names fixed")
