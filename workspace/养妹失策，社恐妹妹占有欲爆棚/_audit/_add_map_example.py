# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\references\example-segment.md"
t = open(p, encoding="utf-8").read()
old = "【资产锁定】\n场景：【S01｜陈诚公寓门口：{场景库：陈诚公寓门口}】"
new = "【资产锁定】\n【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚\n场景：【S01｜陈诚公寓门口：{场景库：陈诚公寓门口}】"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("example updated")
