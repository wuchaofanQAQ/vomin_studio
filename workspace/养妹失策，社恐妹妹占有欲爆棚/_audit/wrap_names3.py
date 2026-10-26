# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 定位裸「手机」
for m in re.finditer(r"(?<!【)手机(?!】)", s):
    print("bare 手机:", repr(s[max(0, m.start()-25):m.start()+8]))

# p01 段的裸「玄关」包上资产名
parts = re.split(r"(?m)^(## 【第\d+段.*?】)$", s)
if len(parts) > 2:
    body = parts[2]
    body = re.sub(r"(?<!【)玄关(?!】)", "【陈诚公寓玄关】", body)
    parts[2] = body
s = "".join(parts)

# 裸手机包上
s = re.sub(r"(?<!【)手机(?!】)", "【手机】", s)
s = s.replace("【【", "【").replace("】】", "】")
open(f, "w", encoding="utf-8").write(s)
print("wrapped")
