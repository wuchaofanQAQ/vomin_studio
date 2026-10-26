# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md"
t = open(p, encoding="utf-8").read()
pairs = [
("【陈诚】的目光从【沈幼怡】的脸移到【双肩书包】，再落到【行李箱】，眉心拧了一下",
 "【陈诚】的目光从画右画外扫到画外下方，眉心拧了一下"),
("下巴朝【行李箱】方向抬了一下", "下巴朝画外下方抬了一下"),
]
for a, b in pairs:
    c = t.count(a)
    print(c, a[:30])
    assert c == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("done")
