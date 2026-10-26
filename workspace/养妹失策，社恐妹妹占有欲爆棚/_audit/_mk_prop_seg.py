# -*- coding: utf-8 -*-
src = open(r"skills\script-to-prompt-30\references\example-segment.md", encoding="utf-8").read()
s = src.replace("【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚",
                "【参考图映射】图1=S01陈诚公寓门口；图2=R01沈幼怡；图3=R02陈诚；图4=P01行李箱")
s = s.replace("道具：【P01｜行李箱：24 寸硬壳，拉杆拉出三十厘米，立在门右地砖上】",
              "道具：【P01｜行李箱：24 寸硬壳，拉杆拉出三十厘米，{道具库：行李箱}】")
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_prop_seg.md", "w", encoding="utf-8").write(s)
