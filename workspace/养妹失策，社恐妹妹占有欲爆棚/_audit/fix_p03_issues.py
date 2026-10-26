# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
t = t.replace('"门内", "门外", "室内", "窗外", "视角", "机位侧",',
              '"门内", "门外", "室内", "窗外", "视角", "机位侧", "前推", "缓推", "后拉", "下压", "跟移",')
open(p, "w", encoding="utf-8").write(t)

f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
pairs = [
("把【行李箱】的硬壳照得发亮", "把【行李箱】的硬壳照得发亮"),
("拉杆上反着一道刺眼的光。", "【行李箱】拉杆上反着一道刺眼的光。"),
("过【陈诚】肩的近景，镜头不动。", "过【陈诚】肩的机位近景，镜头不动。"),
("[18s-20.5s]，【沈幼怡】（OS、偷偷打量说）：「一米八，瘦……就是脾气像只炸毛的猫。」",
 "[18s-21s]，【沈幼怡】（OS、偷偷打量说）：「一米八，瘦，脾气像只炸毛的猫。」"),
("【镜头09｜[20.5s-23s]｜只有一张床】", "【镜头09｜[21s-23s]｜只有一张床】"),
("客厅中景，镜头缓摇过卧室门。", "客厅机位的中景，镜头缓摇过卧室门。"),
("【沈幼怡】手部的特写，静止。", "【沈幼怡】手部机位的特写，静止。"),
("屏幕特写，镜头不动。", "屏幕机位的特写，镜头不动。"),
("【陈诚】的近景，镜头极缓前推。光落在【沈幼怡】的鼻尖上", "【陈诚】的近景，镜头极缓前推。光落在【沈幼怡】的鼻尖上"),
]
for a, b in pairs:
    if s.count(a) == 1:
        s = s.replace(a, b)
    else:
        print("skip:", a[:20])
# p02 裸名
s = s.replace("右手扣住拉杆往上一提", "右手扣住【行李箱】拉杆往上一提")
open(f, "w", encoding="utf-8").write(s)
print("fixed")
