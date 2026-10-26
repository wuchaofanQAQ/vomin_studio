# -*- coding: utf-8 -*-
p = r"skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "- **道具**：左正偏侧、右俯视、绿幕或白底、无文字、材质真实。"
new = "- **道具**：左正偏侧、右正面、绿幕或白底、无文字、材质真实。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("fixed")
