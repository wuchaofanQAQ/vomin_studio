# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
pairs = [
("道具：【P01｜行李箱：拉杆拉出，立在脚边，{道具库：行李箱}】", "道具：【行李箱】：{道具库：行李箱}"),
("待补：【P02｜旧怀表：待补，未读取】", "待补：【旧怀表】（库里没有，待补）"),
("`【第NN段｜00:00-结束｜场景·事件】`", "`【第NN段｜[0s-结束s]｜场景·事件】`"),
("`待补：【P02｜旧怀表：待补，未读取】`", "`待补：【旧怀表】`"),
]
for a, b in pairs:
    c = t.count(a)
    print(c, a[:40])
    if c == 1:
        t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("done")
