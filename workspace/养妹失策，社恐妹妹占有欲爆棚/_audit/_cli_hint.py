# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = "4. 逐集：novel-to-script 转剧本后 write --table 剧本表（见 harness B0a）"
new = "4. 逐集：novel-to-drama 转剧本后 write --table 剧本表（见 harness B0a）"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("cli hint updated")
