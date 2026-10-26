# -*- coding: utf-8 -*-
import re

# 1) 分镜：陈诚的手机不加【】
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
s = s.replace("中景【陈诚】掏出自己的【手机】，拇指往下滑", "中景【陈诚】掏出自己的手机，拇指往下滑")
s = s.replace("切在【陈诚】拇指停在半空、还没抬眼。", "切在【陈诚】拇指停在半空、还没抬眼。")
open(f, "w", encoding="utf-8").write(s)
print("陈诚的手机已去【】")

# 2) 校验器：裸名只查角色（人），道具/场景允许泛指
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
# 找到裸名检查处，限制为角色
m = re.search(r'(\n\s+)(for nm in s\["lock"\]:[^\n]*\n(?:[^\n]*\n){0,6})', t)
print("checker 裸名段落存在:", bool(m))
open(p, "w", encoding="utf-8").write(t)
