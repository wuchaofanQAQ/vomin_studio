# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_script.py"
t = open(p, encoding="utf-8").read()
old = '("OS ≤5", s["os"] <= 5, f"{s[\'os\']}"),'
new = '("OS ≤10（第一人称小说改编，优先保住判断句）", s["os"] <= 10, f"{s[\'os\']}"),'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("OS cap raised to 10")

p = r"skills\novel-to-drama\references\script-format.md"
t = open(p, encoding="utf-8").read()
old2 = "| 内心独白 | `角色（OS）：台词` | 只给主视角，连续不超 2 句 |"
new2 = "| 内心独白 | `角色（OS）：台词` | 只给主视角，连续不超 2 句；全剧单集 ≤10 句（第一人称小说改编，优先保住判断句） |"
assert t.count(old2) == 1
open(p, "w", encoding="utf-8").write(t.replace(old2, new2))
print("format doc updated")
