# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

pairs = [
("硬切中景固定机位。门从内侧拉开一条缝，【陈诚】只露出半张脸，眼睛在门缝里看出去。",
 "硬切中景固定机位。【陈诚】右手扣着门把往里一带，门开一条缝，他侧过身、只露出半张脸，眼睛在门缝里看出去。"),
("硬切全景固定机位。门被拉开，门外白光把门槛压成一条亮线；",
 "硬切全景固定机位。【陈诚】把门再拉开一肩宽，门外白光把门槛压成一条亮线；"),
("硬切中近景固定机位。【沈幼怡】从兜里掏出一部黑色最新款苹果【手机】，玻璃背板在日光下反出一道冷光；",
 "硬切中近景固定机位。【沈幼怡】从【双肩书包】的侧袋里抽出一部黑色最新款苹果【手机】，玻璃背板在日光下反出一道冷光；"),
]
for a, b in pairs:
    assert s.count(a) == 1, a[:30]
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("p01 动作执行人与道具来源已修")
