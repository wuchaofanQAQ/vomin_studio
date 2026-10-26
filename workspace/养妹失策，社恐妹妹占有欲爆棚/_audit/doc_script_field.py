# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\novel-to-drama\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "- 抬头两行：`剧名：XXX` / `第N集　集名`"
new = "- **`完整剧本` 字段只放正文**：从 `1．外景…` 开始；抬头（剧名/集名/对应章节/时长）与集尾 `（本集完）` 都**不进字段**，集名与集数由表格字段承载"
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "- 集尾固定 `（本集完）`"
new2 = "- 集尾**不写** `（本集完）`（只写到最后一句动作或台词）"
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("SKILL 已更新")

p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\novel-to-drama\references\script-format.md"
s = open(p2, encoding="utf-8").read()
print("script-format 含（本集完）:", s.count("（本集完）"))
