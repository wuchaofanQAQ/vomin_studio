# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

pairs = [
# 1) 门铃在门板上约 1.4 米高，贴地仰拍拍不到它
("切镜头，门外贴地仰拍特写，承接【沈幼怡】抬手按下的动作。",
 "切镜头，门外平视特写，机位正对门铃、与圆钮同高，承接【沈幼怡】抬手按下的动作。"),
# 2) 机位先在走廊、又说从门内后拉，自相矛盾
("镜头从门内后拉半步，落幅为二人隔着门槛的双人全景。",
 "镜头在门口向后拉半步，落幅为二人隔着门槛的双人全景。"),
# 3) 入户门向内开，机位在门内会被门板扫到
("切镜头，门内半步的中景，承接【陈诚】话尾。",
 "切镜头，门槛外侧的中景，机位在门外一侧，承接【陈诚】话尾。"),
]
for a, b in pairs:
    assert s.count(a) == 1, a[:24]
    s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("可拍性修正 3 处")
