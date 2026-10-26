# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
before = s.count("{资产库：【")
s = re.sub(r"\{资产库：【([^】]+)】\}", r"{资产库：\1}", s)
s = re.sub(r"（字幕·【([^】]+)】）", r"（字幕·\1）", s)
open(f, "w", encoding="utf-8").write(s)
print("修复锚点内括号:", before)
print("残留 {资产库：【:", s.count("{资产库：【"))
