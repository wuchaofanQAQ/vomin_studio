# -*- coding: utf-8 -*-
# 1) 分镜：p04 镜头10 补字
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
a = "前景是【手机】边缘，中景是他的眼睛，后景是暗客厅。切在他嘴角落下时。"
b = "前景是举在她胸前的【手机】边缘与她的拇指，中景是他的眼睛与鼻梁，后景是暗下来的客厅墙面。切在他嘴角落下、笑意收干净时。"
assert s.count(a) == 1
s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)

# 2) 校验器：字幕行不算资产引用
cp = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(cp, encoding="utf-8").read()
old = '''        masked = re.sub(r"「[^」]*」", "§", masked)  # 引号内是台词/屏幕文字，不是资产引用'''
new = '''        masked = re.sub(r"「[^」]*」", "§", masked)  # 引号内是台词/屏幕文字，不是资产引用
        masked = re.sub(r"（字幕[^）]*）[^\\n]*", "§", masked)  # 字幕行同样是画面内容，不是资产引用'''
assert t.count(old) == 1
t = t.replace(old, new)
open(cp, "w", encoding="utf-8").write(t)
print("fixed")
