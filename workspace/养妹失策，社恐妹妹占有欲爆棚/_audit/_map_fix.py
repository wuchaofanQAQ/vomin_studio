# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\references\example-segment.md"
t = open(p, encoding="utf-8").read()
old = "【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚"
new = "【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚；图4=P01行李箱"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("map fixed")
