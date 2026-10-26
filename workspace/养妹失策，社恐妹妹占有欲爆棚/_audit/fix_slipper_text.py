# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
s = s.replace("旧塑料【黑拖鞋】", "哑光黑塑料【黑拖鞋】")
s = s.replace("42码旧塑料", "42码哑光黑塑料")
s = s.replace("阳台旧铁护栏与晾衣杆", "尽头窗台、窗帘与晾衣杆")
s = s.replace("阳台", "窗边")
open(f, "w", encoding="utf-8").write(s)
print("slipper/scene wording updated; 阳台 remaining:", s.count("阳台"))
