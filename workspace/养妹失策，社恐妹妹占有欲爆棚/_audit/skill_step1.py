# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

pairs = [
("把本集剧本里出现的**角色、场景、道具**逐一对上三张表：",
 "把本集剧本里出现的**角色、场景、道具**逐一对上「资产库」（按 `类型` 区分）："),
("规则：\n\n- **资产表不是出场名单**",
 "规则：\n\n- **绑定前必须先看图**：逐个打开 `文件路径` 指向的图片确认外观（长相、服装、家具位置、光线），再决定这个资产能不能用在本段；不看图不许写分镜。\n- **备注与图一起读**：备注写了反打关系、同源图、近景/中景/远景内容，空间层次照它写。\n- **资产表不是出场名单**"),
]
for a, b in pairs:
    assert t.count(a) == 1, a[:30]
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("Step 1 已补看图规则")
