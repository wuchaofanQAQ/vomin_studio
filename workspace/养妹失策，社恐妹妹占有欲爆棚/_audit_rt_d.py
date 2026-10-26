p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
for a, b in [("【镜头07｜[19s-23s]｜花生米】", "【镜头07｜[19s-23.5s]｜花生米】"),
             ("[19s-23s]，【陈诚】（OS、压着火说）：「嫌他日子", "[19s-23.5s]，【陈诚】（OS、压着火说）：「嫌他日子"),
             ("【镜头08｜[23s-25s]｜松开又攥紧】", "【镜头08｜[23.5s-25s]｜松开又攥紧】")]:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
