import re
s = "【S01｜陈诚公寓门口：{场景库：陈诚公寓门口}】"
print([hex(ord(c)) for c in s[:6]])
print(re.findall(r"【([A-Z]{1,2})(\d{2})", s))
print(re.findall(r"【([A-Z]{1,2})(\d{2})｜", s))
print(re.findall(r"【([A-Z]{1,2})(\d{2})｜([^：】]+)", s))
print(re.findall(r"【([A-Z]{1,2})(\d{2})｜([^：】]+?)(?::([^】]*))?】", s))
