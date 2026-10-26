# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "# Novel to Script — 小说转剧本"
new = "# Novel to Drama — 小说转剧本"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("title updated")
