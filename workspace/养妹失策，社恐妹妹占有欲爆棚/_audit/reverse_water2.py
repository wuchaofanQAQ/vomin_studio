# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

old = "硬切中景固定机位。【陈诚】从画左门洞里端出一只盛着温水的【玻璃杯】，走到茶几边放下，杯底磕出很轻的一声。前景是门洞边缘与他的手，中景是【玻璃杯】，后景是沙发与窗帘。切在杯子放稳、水面还在晃时。"
new = "硬切中景固定机位，反打方向：机位在沙发一侧、朝入户门与开放式厨房。【陈诚】在厨房台面边接了一杯温水，端着【玻璃杯】转身走向茶几，杯底磕出很轻的一声。前景是餐桌边缘与他的手，中景是【玻璃杯】，后景是黑色入户门与玄关柜。切在杯子放稳、水面还在晃时。"
assert s.count(old) == 1
s = s.replace(old, new)

old2 = "节奏：开场【陈诚公寓客厅（反打玄关）】只占六秒（拖鞋—水—走向窗边），其余全在窗边对白，每句一刀。"
new2 = "节奏：开场【陈诚公寓客厅（反打玄关）】只占六秒（拖鞋—水—走向窗边），倒水一镜切到沙发一侧的反打，其余全在窗边对白，每句一刀。"
assert s.count(old2) == 1
s = s.replace(old2, new2)

open(f, "w", encoding="utf-8").write(s)
print("p03 倒水改为反打")
