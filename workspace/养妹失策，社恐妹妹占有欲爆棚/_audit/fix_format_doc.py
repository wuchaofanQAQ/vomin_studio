# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\novel-to-drama\references\script-format.md"
s = open(p, encoding="utf-8").read()
print("before:", s.count("（本集完）"), "处")
# 删掉模板里的整行
s = "\n".join(l for l in s.splitlines() if l.strip() != "（本集完）")
# 规则句改写
s = s.replace("集尾固定 `（本集完）`", "集尾不写 `（本集完）`")
s = s.replace("（本集完）", "")
open(p, "w", encoding="utf-8").write(s)
print("after:", s.count("（本集完）"))
