# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

pairs = [
("十二镜按下列时码依次硬切，平均每镜两秒；",
 "十二镜按下列时码依次硬切，平均每镜约二点三秒；本段台词密度低、以反应与停顿为主，故意不切碎（偏离对白戏 1.5–1.8 秒的参考区间，属有意选择）。"),
("十三镜按下列时码依次硬切，平均每镜两秒多；",
 "十三镜按下列时码依次硬切，平均每镜约二点二秒；本段落在“认亲—拒绝”的慢节拍上，靠长一点的反应镜头压住情绪（偏离对白戏参考区间，属有意选择）。"),
]
for a, b in pairs:
    assert s.count(a) == 1, a[:20]
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("已写入节奏偏离说明")
