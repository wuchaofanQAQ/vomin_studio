# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

old = "正面机位的屏幕特写，静止。走廊的蝉声退成一层底噪，屏幕的冷白把四周压得更黑。米白底上跳出「妈妈说，给你发过信息了。」，末尾一个没删掉的句号，光标一闪一闪；【沈幼怡】的指腹悬在发送键上方，没有按下去。切在这行字亮着、她还没按。"
new = "过【陈诚】肩的机位近景，镜头轻推。走廊的蝉声退成一层底噪。中景【沈幼怡】又把【手机】翻转过来、屏幕对着他；微信聊天框里那行字大得出格：「妈妈说，给你发过信息了。」，末尾一个没删掉的句号，光标还在闪；冷白的光把【陈诚】的半张脸照出来，另半边沉在门缝的暗里。切在屏幕举稳、他眼睛动了一下。"
assert s.count(old) == 1
s = s.replace(old, new)
open(f, "w", encoding="utf-8").write(s)
print("镜头12 也改为翻屏")
