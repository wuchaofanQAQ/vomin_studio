# -*- coding: utf-8 -*-
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
s = s.replace("【陈诚公寓【陈诚公寓玄关】傍晚】", "【陈诚公寓玄关傍晚】")
s = s.replace("【陈诚公寓【陈诚公寓玄关】】", "【陈诚公寓玄关】")
s = s.replace("陈诚公寓【陈诚公寓玄关】傍晚", "陈诚公寓玄关傍晚")
open(f, "w", encoding="utf-8").write(s)
print("嵌套修复完成，残留:", s.count("【陈诚公寓【"))
