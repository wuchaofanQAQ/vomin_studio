import re
ENTRY_RE = re.compile(r"【([A-Z]{1,2})(\d{2})｜([^：】]+?)(?::([^】]*))?】")
lines = [
 "【S01｜陈诚公寓门口：{场景库：陈诚公寓门口}】",
 "【R01｜沈幼怡：{角色库：沈幼怡}】【R02｜陈诚：{角色库：陈诚}】",
 "【P01｜行李箱：24 寸硬壳，拉杆拉出三十厘米】",
]
for s in lines:
    print(repr(s[:20]), ENTRY_RE.findall(s))
