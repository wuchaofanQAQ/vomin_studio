# -*- coding: utf-8 -*-
src = open(r"skills\script-to-prompt-30\references\example-segment.md", encoding="utf-8").read()
import re
# 1) 删掉映射行
a = src.replace("【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚\n", "")
# 2) 顺序写反
b = src.replace("图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚",
                "图1=R02陈诚；图2=R01沈幼怡；图3=S01陈诚公寓门口")
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_no_map.md", "w", encoding="utf-8").write(a)
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_wrong_map.md", "w", encoding="utf-8").write(b)
